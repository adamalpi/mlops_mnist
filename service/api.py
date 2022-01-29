import connexion
from PIL import Image

from inference import Model


def inference(experiment_name: str) -> dict:
    """Hook function that responds to api/inference.

    This function runs a prediction for the <experiment_name> and the image
    passed in the body of the request.

    Args:
        experiment_name: name of the experiment, which will help finding the 
        right model for inferencing

    Returns:
        payload with the prediction.
    """
    uploaded_file = connexion.request.files["image_blob"]

    prediction = _inference(experiment_name, uploaded_file)

    result = {"class": prediction}

    return result


def _inference(experiment_name: str, uploaded_file):
    model = Model(experiment_name)

    image = Image.open(uploaded_file)
    prediction = model.inference(image)

    return prediction
