SHELL := /bin/bash

# Extract version from pyproject.toml, with fallback if not found
VERSION := $(shell grep -m 1 version pyproject.toml | tr -s ' ' | tr -d '"' | tr -d "'" | cut -d' ' -f3)
ifndef VERSION
$(error Version not found in pyproject.toml)
endif

IMAGE_NAME := paddleocr-docker
DOCKER_USER := thomaskuoch

.PHONY: build start stop test push clean prune

# Build the Docker image with the specified version
build:
	docker build --platform="linux/amd64" -t $(IMAGE_NAME):$(VERSION) .

# Start the container
start:
	docker run -d --name $(IMAGE_NAME) -p 8866:8866 --shm-size=1gb $(IMAGE_NAME):$(VERSION)

# Stop the container if it's running
stop:
	docker stop $(IMAGE_NAME) || true
	docker rm $(IMAGE_NAME) || true

# Test the image with Pytest
test: 
	docker build -t $(IMAGE_NAME):test .
	docker run --rm --entrypoint /bin/sh $(IMAGE_NAME):test -c "uv run pytest ./test.py"
	docker rmi $(IMAGE_NAME):test

# Tag and push the Docker image to the repository
push:
	docker tag $(IMAGE_NAME):$(VERSION) $(DOCKER_USER)/$(IMAGE_NAME):$(VERSION)
	docker tag $(IMAGE_NAME):$(VERSION) $(DOCKER_USER)/$(IMAGE_NAME):latest
	docker push $(DOCKER_USER)/$(IMAGE_NAME):$(VERSION)
	docker push $(DOCKER_USER)/$(IMAGE_NAME):latest

# Clean up local images
clean:
	docker rmi $(IMAGE_NAME):$(VERSION) || true
	docker rmi $(DOCKER_USER)/$(IMAGE_NAME):$(VERSION) || true
	docker rmi $(DOCKER_USER)/$(IMAGE_NAME):latest || true

# Remove dangling images and stopped containers to free space
prune:
	docker system prune -f

# Utility target to display available Makefile commands
help:
	@echo "Available commands:"
	@echo "  make build     - Build the Docker image"
	@echo "  make start     - Start the Docker container"
	@echo "  make stop      - Stop and remove the Docker container"
	@echo "  make test      - Run tests in a test container"
	@echo "  make push      - Push the Docker image to Docker Hub"
	@echo "  make clean     - Remove built Docker images"
	@echo "  make prune     - Remove unused Docker data"
	@echo "  make help      - Show this help message"
