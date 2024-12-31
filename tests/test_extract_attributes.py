from fastapi.testclient import TestClient


def test_extract_attributes(client: TestClient) -> None:
    sku = "Simple Lamp FKD54104/126W 900*580 grey"
    r = client.get("/attributes", params={"sku": sku})
    assert r.status_code == 200
    attributes = r.json()
    assert attributes
    assert attributes["name"] == "Simple Lamp"
    assert attributes["serial_number"] == "FKD54104"
    assert attributes["wattage"] == "126W"
    assert attributes["size"] == "900*580"
    assert attributes["color"] == "grey"
