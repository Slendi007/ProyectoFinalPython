from fastapi.testclient import TestClient


def login(
    client: TestClient,
) -> str:
    response = client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "admin123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

    return str(data["access_token"])


def test_orders_complete_flow(
    client: TestClient,
) -> None:
    token = login(client)

    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/orders",
        headers=headers,
        json={
            "id": 1,
            "customer": "Cesar",
            "items": [
                {
                    "product": "Laptop",
                    "quantity": 1,
                    "unit_price": 15000,
                },
                {
                    "product": "Mouse",
                    "quantity": 2,
                    "unit_price": 350,
                },
            ],
        },
    )

    assert create_response.status_code == 201

    created_order = create_response.json()

    assert created_order["id"] == 1
    assert created_order["customer"] == "Cesar"

    get_response = client.get(
        "/orders/1",
        headers=headers,
    )

    assert get_response.status_code == 200

    order = get_response.json()

    assert order["id"] == 1
    assert order["customer"] == "Cesar"
    assert len(order["items"]) == 2

    list_response = client.get(
        "/orders",
        headers=headers,
    )

    assert list_response.status_code == 200

    orders = list_response.json()

    assert len(orders) == 1
    assert orders[0]["id"] == 1

    delete_response = client.delete(
        "/orders/1",
        headers=headers,
    )

    assert delete_response.status_code == 200

    assert delete_response.json() == {"message": "Orden 1 eliminada"}

    missing_response = client.get(
        "/orders/1",
        headers=headers,
    )

    assert missing_response.status_code == 404


def test_orders_requires_authentication(
    client: TestClient,
) -> None:
    response = client.get("/orders")

    assert response.status_code == 401


def test_invalid_token_is_rejected(
    client: TestClient,
) -> None:
    response = client.get(
        "/orders",
        headers={"Authorization": ("Bearer token-invalido")},
    )

    assert response.status_code == 401

    assert response.json() == {"detail": "Token inválido o expirado"}


def test_login_with_invalid_password(
    client: TestClient,
) -> None:
    response = client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "incorrecta",
        },
    )

    assert response.status_code == 401

    assert response.json() == {"detail": ("Usuario o contraseña incorrectos")}


def test_create_order_with_invalid_quantity(
    client: TestClient,
) -> None:
    token = login(client)

    response = client.post(
        "/orders",
        headers={"Authorization": (f"Bearer {token}")},
        json={
            "id": 1,
            "customer": "Cesar",
            "items": [
                {
                    "product": "Laptop",
                    "quantity": 0,
                    "unit_price": 15000,
                }
            ],
        },
    )

    assert response.status_code == 422
