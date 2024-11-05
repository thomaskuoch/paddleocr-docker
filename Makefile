build:
	docker build -t paddleocr-docker .

start:
	docker run -it --rm --entrypoint bash -p 8866:8866 paddleocr-docker