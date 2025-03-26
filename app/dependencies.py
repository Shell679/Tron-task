from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import AsyncTron

from app.config.database import async_session_maker
from app.v1.repositories.wallet_repository import WalletRepository
from app.v1.services.wallet_service import WalletService

tron_client = AsyncTron(network="nile")


async def get_async_session():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_wallet_service(session: AsyncSession = Depends(get_async_session)) -> WalletService:
    wallet_repository = WalletRepository(session)
    return WalletService(wallet_repository, tron_client)