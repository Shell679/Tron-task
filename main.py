import uvicorn

from app.api.v1.routers.wallet_router import router as wallet_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(wallet_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)