# PaddleOCR Docker

This project provides a Docker image to easily run PaddleOCR as a service.

## Usage Instructions

### Pull the Image
To get the latest version of the PaddleOCR Docker image:
```bash
docker pull thomaskuoch/paddleocr-docker:latest
```

### Start the Container
Run the container, mapping it to port 8866:
```bash
docker run -d -p 8866:8866 thomaskuoch/paddleocr-docker:latest
```

### Sending an OCR Request

The PaddleOCR service expects a POST request with a base64-encoded image. Here’s how to send an OCR request using `curl`:

```bash
curl -X POST \
    'http://localhost:8866/ocr' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'filedata=<base64_image>'
```

Or, you can encode an image in base64 and send the request with Python:

```python
import base64
import requests

with open("image.jpg", "rb") as f:
    image_data = f.read()

image_encoded = base64.b64encode(image_data).decode()
payload = {"filedata": image_encoded}
response = requests.post("http://localhost:8866/ocr", data=payload).json()

print(response)
```

### Sample Response

The response includes OCR results, with bounding box coordinates and recognized text. An example response structure:

```json
{
    "ocr_result": [
        [
            [
                [
                    [387, 49],
                    [533, 49],
                    [533, 82],
                    [387, 82]
                ],
                ["UTOPIA", 0.9971577525138855]
            ]
        ]
    ]
}
```

In this example:
- `"ocr_result"` contains the detected text along with coordinates of the bounding box.
- Each box shows the detected text along with a confidence score.