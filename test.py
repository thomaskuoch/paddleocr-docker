import base64

from fastapi.testclient import TestClient

from main import app
from rotate import infer_angle

client = TestClient(app)


def test_ocr_jpg():
    _test_ocr("./data/example.jpg")


def test_ocr_png():
    _test_ocr("./data/example.png")


def test_ocr_rotated():
    _test_ocr("./data/example_rotated.jpg")


def test_infer_angle():
    angle = infer_angle("./data/example_rotated.jpg")
    assert abs(angle) == 90


def _test_ocr(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    payload = {"filedata": encoded}
    resp = client.post("/ocr", data=payload).json()
    texts = [text for _, (text, _) in resp["ocr_result"][0]]
    assert texts[-2:] == [
        "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<",
        "L898902C36UT07408122F1204159ZE184226B<<<<<10",
    ]
