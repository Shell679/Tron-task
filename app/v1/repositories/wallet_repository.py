from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import TronWallet
from app.schemas.schema import WalletCreate, WalletRead


class WalletRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_wallets(self) -> Sequence[WalletRead]:
        data = await self.session.execute(select(TronWallet))
        wallets = data.scalars().all()

        return wallets

    async def create_wallet_query(self, new_wallet_data: WalletCreate) -> dict[str, Any]:
        new_wallet = TronWallet(**new_wallet_data.model_dump())
        self.session.add(new_wallet)
        await self.session.flush()
        await self.session.commit()

        return new_wallet_data.model_dump()
