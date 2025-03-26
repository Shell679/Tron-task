from pydantic import BaseModel

class WalletCreate(BaseModel):
    wallet_address: str
    balance: float
    bandwidth: int
    energy: int

class WalletResponse(WalletCreate):
    pass