import io
from PIL import Image

from api import _inference


def _serialize_image(image: Image) -> io.BytesIO:
    byte_img_buffer = io.BytesIO()
    image.save(byte_img_buffer, "PNG")
    byte_img_buffer.seek(0)
    return byte_img_buffer


def test_inference():
    experiment = "fashion_mnist_experiment_10__0.001_0.5"
    with Image.open("../data/5523.png") as image:
        image_buffer = _serialize_image(image)
        prediction = _inference(experiment, image_buffer)

    assert prediction == "Sneaker"
