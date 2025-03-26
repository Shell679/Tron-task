from datetime import datetime

from pydantic import BaseModel, field_serializer


class WalletRead(BaseModel):
    id: int
    wallet_address: str
    balance_trx: float
    bandwidth: int
    energy: int
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime) -> str:
        return created_at.strftime("%Y-%m-%d %H:%M:%S")

class WalletCreate(BaseModel):
    wallet_address: str
    balance_trx: float
    bandwidth: int
    energy: int

class WalletResponse(BaseModel):
    balance_trx: float
    bandwidth: int
    energy: int