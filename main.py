import base64
import io
import os
from typing import Union

import numpy as np
import uvicorn
from fastapi import FastAPI, Form, HTTPException
from paddleocr import PaddleOCR
from PIL import Image

OCR_MODEL = PaddleOCR(lang="fr", use_angle_cls=True)

app = FastAPI()


def do_ocr(image: Union[Image.Image, np.ndarray]):
    """Perform OCR on the given image."""
    return OCR_MODEL.ocr(image, cls=True)


@app.post("/ocr")
async def ocr_endpoint(filedata: str = Form(...)):
    try:
        img_recovered = decode_b64(filedata)
        img = Image.open(io.BytesIO(img_recovered)).convert("RGB")
        ocr_result = do_ocr(np.array(img))
        return {"ocr_result": ocr_result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=500, detail="An error occurred during OCR processing."
        )


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


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8866)),
    )
