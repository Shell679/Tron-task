from unittest.mock import AsyncMock

import pytest

@pytest.mark.asyncio
async def test_get_wallets_endpoint(mocker):
    mock_response = AsyncMock()
    mock_response.json = AsyncMock(return_value=[
        {"wallet_address": "wallet_address_test", "bandwidth": 1000, "energy": 500, "balance_trx": 10.5}
    ])
    mock_response.status_code = 200

    mock_get = mocker.patch("httpx.AsyncClient.get", return_value=mock_response)

    response = await mock_get("/api/v1/wallets")

    assert response.status_code == 200
    data = await response.json()
    assert data[0]["wallet_address"] == "wallet_address_test"

@pytest.mark.asyncio
async def test_create_wallet_endpoint(async_client, mock_wallet_service, monkeypatch):
    monkeypatch.setattr("app.api.v1.routers.wallet_router.get_wallet_service", lambda: mock_wallet_service)

    response = await async_client.post("/api/v1/wallets/wallet_address_test")

    assert response.status_code == 200
    assert response.json() == {
        "balance_trx": 100.0,
        "bandwidth": 5000,
        "energy": 3000
    }
