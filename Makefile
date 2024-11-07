build:
	docker build -t paddleocr-docker .

start:
	docker run -it --rm -p 8866:8866 paddleocr-docker

test: 
	docker build -t paddleocr-docker-test .
	docker run --rm --entrypoint /bin/sh paddleocr-docker-test -c "uv run pytest ./test.py"
	docker rmi paddleocr-docker-test