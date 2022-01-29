from inference import Model
from PIL import Image


def test_inference():
    model = Model("fashion_mnist_experiment_10__0.001_0.5", root_dir='..')
    with Image.open("../../data/5523.png") as image:
        prediction = model.inference(image)

    assert prediction == "Sneaker"
