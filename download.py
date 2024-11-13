from loguru import logger
from paddleocr import PaddleOCR

if __name__ == "__main__":
    # https://github.com/PaddlePaddle/PaddleOCR/issues/11530#issuecomment-2017651736
    logger.info("Downloading PaddleOCR files...")
    PaddleOCR(lang="fr", use_angle_cls=True, det_db_score_mode="slow")
