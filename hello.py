import os
from uuid import uuid4

import cv2
from paddleocr import PaddleOCR

model = PaddleOCR(lang="fr", use_angle_cls=True)


def do_ocr(filename):
    if filename.lower().endswith(".png"):
        converted_filename = convert_png_to_jpg(filename)
        result = model.ocr(converted_filename, cls=True)
        os.remove(converted_filename)
    else:
        result = model.ocr(filename, cls=True)
    return result


def convert_png_to_jpg(filename):
    """Convert a PNG image to a high-quality JPG image."""
    assert filename.lower().endswith(".png"), "Input file must be .png"
    image = cv2.imread(filename)
    converted_filename = f"{uuid4()}.jpg"
    cv2.imwrite(converted_filename, image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    return converted_filename


if __name__ == "__main__":
    print(do_ocr("example.jpg"))
    print(do_ocr("example.png"))
