from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import AsyncTron
from tronpy.providers import AsyncHTTPProvider

from app.config.database import async_session_maker
from app.api.v1.repositories.wallet_repository import WalletRepository
from app.api.v1.services.wallet_service import WalletService
from app.config.env_config import API_KEY

tron_client = AsyncTron(
        provider=AsyncHTTPProvider(
            "https://api.trongrid.io",
            api_key=API_KEY,
        )
    )


async def get_async_session():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_wallet_service(session: AsyncSession = Depends(get_async_session)) -> WalletService:
    wallet_repository = WalletRepository(session)
    return WalletService(wallet_repository, tron_client)