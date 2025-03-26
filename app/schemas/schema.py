from datetime import datetime

from pydantic import BaseModel

class WalletRead(BaseModel):
    id: int
    wallet_address: str
    balance: float
    bandwidth: int
    energy: int
    created_at: datetime

class WalletCreate(BaseModel):
    wallet_address: str
    balance: float
    bandwidth: int
    energy: int

class WalletResponse(WalletCreate):
    pass