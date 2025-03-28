from unittest.mock import AsyncMock

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.api.v1.repositories.wallet_repository import WalletRepository
from app.api.v1.services.wallet_service import WalletService
from app.config.env_config import DB_USER, DB_HOST, DB_PASS, DB_PORT, DB_TEST_NAME
from app.dependencies import get_wallet_service
from main import app

TEST_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_TEST_NAME}"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture
async def test_db():
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def wallet_repo(test_db: AsyncSession):
    return WalletRepository(test_db)

@pytest_asyncio.fixture
async def mock_wallet_service():
    mock_service = AsyncMock(spec_set=WalletService)
    mock_service.process_wallet_request = AsyncMock()
    mock_service.process_wallet_request.return_value = {
        "wallet_address": "wallet_address_test",
        "balance_trx": 100.0,
        "bandwidth": 5000,
        "energy": 3000
    }
    return mock_service

@pytest_asyncio.fixture
async def async_client(mock_wallet_service):
    app.dependency_overrides[get_wallet_service] = lambda: mock_wallet_service
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()