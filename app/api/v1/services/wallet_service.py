from typing import Optional, Sequence

from fastapi import HTTPException
from tronpy import AsyncTron
from tronpy.exceptions import AddressNotFound

from app.schemas.schema import WalletCreate, WalletRead
from app.api.v1.repositories.wallet_repository import WalletRepository

class WalletService:
    def __init__(self, wallet_repository: WalletRepository, tron_client: AsyncTron) -> None:
        self.wallet_repository = wallet_repository
        self.tron_client = tron_client

    async def get_wallets(self) -> Sequence[WalletRead]:
        return await self.wallet_repository.get_wallets()

    async def get_wallet_info(self, wallet_address: str) -> Optional[dict]:
        try:
            account = await self.tron_client.get_account(wallet_address)

            balance_trx = account.get("balance", 0) / 1_000_000

            resources = await self.tron_client.get_account_resource(wallet_address)

            bandwidth = resources.get("NetLimit", 0) + resources.get("freeNetLimit", 0)
            energy = resources.get("EnergyLimit", 0)

            return {"wallet_address": wallet_address, "balance_trx": balance_trx, "bandwidth": bandwidth, "energy": energy}

        except Exception as e:
            if e == AddressNotFound:
                raise HTTPException(status_code=404, detail="Кошелек не найден")
            raise HTTPException(status_code=500, detail=f"Упс... что-то пошло не так")

    async def process_wallet_request(self, wallet_address: str):
        wallet_data = await self.get_wallet_info(wallet_address)

        wallet_schema = WalletCreate(**wallet_data)

        return await self.wallet_repository.create_wallet_query(wallet_schema)
