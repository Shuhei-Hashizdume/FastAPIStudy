def test_cors_preflight_allows_configured_origin():
    from tests.support import client

    response = client.options(
        "/books/1",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "PATCH",
            "Access-Control-Request-Headers": "Authorization",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert "PATCH" in response.headers["access-control-allow-methods"]
    assert "Authorization" in response.headers["access-control-allow-headers"]


def test_cors_preflight_rejects_unconfigured_origin():
    from tests.support import client

    response = client.options(
        "/books/1",
        headers={
            "Origin": "http://localhost:4000",
            "Access-Control-Request-Method": "PATCH",
            "Access-Control-Request-Headers": "Authorization",
        },
    )
    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


def test_cors_adds_allow_origin_header_to_actual_response(authenticated_client):

    response = authenticated_client.get(
        "/books",
        headers={
            "Origin": "http://localhost:3000",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
