import pytest

from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from app.api.v1.repositories.wallet_repository import WalletRepository
from app.models.models import TronWallet
from app.schemas.schema import WalletCreate, WalletRead
from datetime import datetime


@pytest.mark.asyncio
async def test_get_wallets_query(mocker):
    fake_wallets = [
        TronWallet(id=1, wallet_address="wallet_1", bandwidth=2000, energy=1000, balance_trx=50.0,
                   created_at=datetime.utcnow()),
        TronWallet(id=2, wallet_address="wallet_2", bandwidth=1500, energy=800, balance_trx=30.0,
                   created_at=datetime.utcnow()),
    ]

    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = AsyncMock(spec=Result)
    mock_result.scalars.return_value.all.return_value = fake_wallets
    mock_session.execute.return_value = mock_result

    wallet_repo = WalletRepository(mock_session)

    result = await wallet_repo.get_wallets()

    mock_session.execute.assert_called_once()

    assert len(result) == 2
    assert result[0].wallet_address == "wallet_1"
    assert result[1].wallet_address == "wallet_2"

    assert all(isinstance(wallet, WalletRead) for wallet in result)


@pytest.mark.asyncio
async def test_create_wallet_query():
    wallet_repo = WalletRepository(None)
    wallet_repo.create_wallet_query = AsyncMock(return_value={"wallet_address": "wallet_address_test"})

    wallet_data = WalletCreate(
        wallet_address="wallet_address_test",
        bandwidth=1000,
        energy=500,
        balance_trx=10.5
    )

    result = await wallet_repo.create_wallet_query(wallet_data)

    assert result["wallet_address"] == wallet_data.wallet_address

