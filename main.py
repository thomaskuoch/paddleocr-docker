import base64
import io
import os

import numpy as np
import uvicorn
from fastapi import FastAPI, Form
from paddleocr import PaddleOCR
from PIL import Image

OCR_MODEL = PaddleOCR(lang="fr", use_angle_cls=True)

app = FastAPI()


def do_ocr(image):
    return OCR_MODEL.ocr(image, cls=True)


@app.post("/ocr")
def ocr_endpoint(filedata: str = Form(...)):
    img_recovered = decode_b64(filedata)
    img = Image.open(io.BytesIO(img_recovered)).convert("RGB")
    img_array = np.array(img)
    ocr_result = do_ocr(img_array)
    return ocr_result


def decode_b64(content: str) -> bytes:
    if (
        content.startswith("data:image/jpeg")
        or content.startswith("data:image/jpg")
        or content.startswith("/9")
    ):
        content = content[content.find("/9") :]
    elif content.startswith("data:image/png") or content.startswith("iVBO"):
        content = content[content.find("iVBO") :]
    else:
        raise ValueError("only jpeg and png are valid")
    return base64.b64decode(content)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", 8866)),
    )
