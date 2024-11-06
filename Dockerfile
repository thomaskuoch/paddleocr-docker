FROM python:3.10.15-slim

# Install system dependencies in a single step to minimize layers and clean up afterwards
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    ca-certificates \
    libgl1 \
    libgomp1 \
    libglib2.0-0 \
    poppler-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download and install uv in one step, then clean up the installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Update the PATH environment variable
ENV PATH="/root/.cargo/bin/:$PATH"

# Set the working directory
WORKDIR /app

# Copy only the necessary files for dependency installation
COPY uv.lock pyproject.toml ./
# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Run PaddleOCR setup using a single command
RUN uv run python -c "from paddleocr import PaddleOCR; PaddleOCR(lang='fr', use_angle_cls=True)"

# Copy the remaining application code
COPY . .

# Use bash as the entry point
CMD ["uv", "run", "python", "/app/main.py"]
