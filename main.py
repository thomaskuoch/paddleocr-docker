import base64
import io
import os
from typing import Union

import numpy as np
import uvicorn
from fastapi import FastAPI, Form, HTTPException
from paddleocr import PaddleOCR
from PIL import Image

from rotate import infer_angle, rotate

OCR_MODEL = PaddleOCR(lang="fr", use_angle_cls=True, det_db_score_mode="slow")

app = FastAPI()

with open("./data/example.txt", "r") as f:
    example_base64_image = f.read()


@app.get("/")
async def root():
    return {"service": "paddleocr-docker", "version": read_version()}


@app.post("/ocr")
async def ocr_endpoint(
    filedata: str = Form(
        default=example_base64_image,
        description="Base64 encoded image",
    ),
):
    try:
        img_recovered = decode_b64(filedata)
        img = Image.open(io.BytesIO(img_recovered)).convert("RGB")
        img_array = np.array(img)
        img_array = rotate_if_necessary(img_array)
        ocr_result = do_ocr(img_array)
        return {"ocr_result": ocr_result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=500, detail="An error occurred during OCR processing."
        )


def do_ocr(image: Union[Image.Image, np.ndarray]):
    """Perform OCR on the given image."""
    return OCR_MODEL.ocr(image, cls=True)


def decode_b64(content: str) -> bytes:
    """Decode base64 image content."""
    try:
        if content.startswith("data:image"):
            comma_index = content.find(",")
            if comma_index != -1:
                content = content[comma_index + 1 :]
        return base64.b64decode(content)
    except Exception as e:
        raise ValueError("Failed to decode base64 image content: " + str(e))


def rotate_if_necessary(img_array: np.ndarray) -> np.ndarray:
    """Rotate the image if the text is vertical."""
    angle = abs(infer_angle(img_array))
    if 60 < angle < 120:
        img_array = rotate(img_array, 90)
    return img_array


def read_version():
    with open("pyproject.toml", "r") as f:
        lines = f.readlines()
        for line in lines:
            if "version" in line:
                return line.split("=")[1].strip().replace('"', "")


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8866)),
    )
