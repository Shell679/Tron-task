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

        wallet_dicts = [wallet.__dict__ for wallet in wallets]
        return [WalletRead.model_validate(wallet) for wallet in wallet_dicts]

    async def create_wallet_query(self, new_wallet_data: WalletCreate) -> dict[str, Any]:
        new_wallet = TronWallet(**new_wallet_data.model_dump())
        self.session.add(new_wallet)
        await self.session.commit()
        await self.session.refresh(new_wallet)

        return new_wallet_data.model_dump()
