FROM python:3.10.15-slim

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y build-essential curl ca-certificates libgl1 libgomp1 libglib2.0-0 poppler-utils

# install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.cargo/bin/:$PATH"

WORKDIR /app
COPY uv.lock pyproject.toml ./
RUN uv sync --frozen
RUN uv run python -c 'from paddleocr import PaddleOCR; PaddleOCR(lang="fr", use_angle_cls=True)'

COPY . .

ENTRYPOINT ["/bin/bash"]