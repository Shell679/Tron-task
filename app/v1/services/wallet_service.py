from typing import Optional
from tronpy import AsyncTron

from app.schemas.schema import WalletCreate
from app.v1.repositories.wallet_repository import WalletRepository


class WalletService:
    def __init__(self, wallet_repository: WalletRepository, tron_client: AsyncTron) -> None:
        self.wallet_repository = wallet_repository
        self.tron_client = tron_client

    async def get_wallet_info(self, wallet_address: str) -> Optional[dict]:
        try:
            account = await self.tron_client.get_account(wallet_address)
            balance = account.get("balance", 0) / 1_000_000
            resources = await self.tron_client.get_account_resource(wallet_address)
            bandwidth = resources.get("freeNetLimit", 0)
            energy = resources.get("EnergyLimit", 0)

            return {"wallet_address": wallet_address, "balance": balance, "bandwidth": bandwidth, "energy": energy}
        except Exception:
            return None

    async def process_wallet_request(self, wallet_address: str):
        wallet_data = await self.get_wallet_info(wallet_address)
        if not wallet_data:
            return None

        wallet_schema = WalletCreate(**wallet_data)
        return await self.wallet_repository.create_wallet_query(wallet_schema)