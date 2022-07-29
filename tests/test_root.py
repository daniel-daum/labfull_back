from conftest import client

def test_root(client):
    res = client.get("/")

    assert res.status_code == 200
    assert res.json().get('Root') == "API documentation is located at http://www.localhost:8000/docs"

