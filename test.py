import base64

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_ocr_jpg():
    do_ocr_img_path("./data/example.jpg")


def test_ocr_png():
    do_ocr_img_path("./data/example.png")


def do_ocr_img_path(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    payload = {"filedata": encoded}
    resp = client.post("/ocr", data=payload)
    assert resp.status_code == 200
