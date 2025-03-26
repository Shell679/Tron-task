from typing import List

from fastapi import APIRouter, Depends

from app.dependencies import get_wallet_service
from app.schemas.schema import WalletRead, WalletResponse
from app.api.v1.services.wallet_service import WalletService

router = APIRouter(
    tags=["Wallet"],
    prefix="/api/v1"
)

@router.get("/wallets", response_model=List[WalletRead])
async def get_wallets(wallet_service: WalletService = Depends(get_wallet_service)):
    return await wallet_service.get_wallets()

@router.post("/wallets/{wallet_address}", response_model=WalletResponse)
async def create_wallet(wallet_address: str, wallet_service: WalletService = Depends(get_wallet_service)):
    return await wallet_service.process_wallet_request(wallet_address)
