import json

import pandas as pd
import requests
import streamlit as st

from sql.df_management import DBManager
from sql.query_lib import get_all_experiments


# DB info
DB_HOST = "db"
DB_NAME = "mlopsdb"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = "pass123"

# Inference backend info
INFERENCE_URI = "http://backend:9090/api/v1.0/inference"


def query_experiments_data() -> pd.DataFrame:
    """Loads info of all experiments in memory.
    
    Data is transformed into a format that is more suitable for the visualization.
    """
    db_manager = DBManager(
        db_host=DB_HOST,
        db_name=DB_NAME,
        db_port=DB_PORT,
        db_user=DB_USER,
        db_password=DB_PASSWORD,
    )
    df_experiments = get_all_experiments(db_manager)
    return df_experiments


def _process_raw_experiment_data(df: pd.DataFrame) -> pd.DataFrame:
    # define ID of the data points
    df["ID"] = df["Experiment Name"].str.split("__", expand=True)[0]
    df["ID"] = df["ID"].str.replace("fashion_mnist_experiment_", "")
    df["ID"] = df["ID"].astype(int)
    df.set_index("ID", inplace=True)
    df.sort_index(inplace=True)

    def _parse_loss(loss):
        if type(loss) == str:
            loss = json.loads(loss)
        loss_vector = loss["Value"]
        return loss_vector

    # extract losses vector for each experiment
    df["Loss Vector"] = df["Loss"].apply(_parse_loss)

    return df


def expand_losses(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts losses of the experiments into an independent dataframe.

    Args:
        df: experiment data.

    Returns:
        new df for losses.
    """
    first_loss = df["Loss"].iloc[0]
    if isinstance(first_loss, str):
        steps = json.loads(df["Loss"].iloc[0])["Step"]
    else:
        steps = first_loss["Step"]

    # transpose to have the steps in the y axis.
    df_losses = pd.DataFrame(df["Loss Vector"].to_list(), columns=steps).T
    df_losses.columns = df.index.to_list()

    return df_losses


def predict_all(image, experiments) -> pd.DataFrame:
    """Run predictions for a given <image>.

    Args:
        image (io.IOBytes): image used for running predictions.
        experiments (List[str]): list of experiments for which to run predictions.

    Returns:
        A dataframe that contains predictions for all experiments.
    """
    predictions = {}
    for experiment in experiments:
        predict_class = _predict(image, experiment)
        predictions[experiment] = predict_class

    df_predictions = pd.DataFrame.from_dict([predictions]).T
    df_predictions.columns = ["Predictions"]
    df_predictions.rename_axis("Experiment Name")

    return df_predictions


def _predict(image, experiment) -> str:
    image.seek(0)
    url = f"{INFERENCE_URI}?experiment_name={experiment}"

    files = {"image_blob": image}
    result = requests.post(url, files=files)

    pred_result = result.json()
    return pred_result["class"]


if __name__ == "__main__":
    st.title("MLOps for MNIST")

    # Read data
    df = query_experiments_data()

    # Configure default sidebar options based on data.
    n_experiments = st.sidebar.number_input(
        "Show latest X experiments. Select X.",
        min_value=1,
        max_value=len(df),
        value=(5 if len(df) > 5 else len(df)),
    )

    experiments_id = df.index.to_list()
    default_experiments = experiments_id[-n_experiments:]
    options = st.sidebar.multiselect(
        "Or would you rather select yourself the experiments?", experiments_id, default_experiments
    )

    # Visualize data
    df_extract = df[["Experiment Name", "Learning Rate", "Momentum"]]
    df_extract = df_extract[df.index.isin(options)]
    df_extract.sort_index(inplace=True)
    st.write(df_extract.sort_index())

    st.subheader("View of losses")
    df_losses = expand_losses(df)
    st.line_chart(df_losses[options])

    # Prediction section.
    # When an image is uploaded, all selected experiments will return their prediction for that image.
    st.subheader("Predict")
    uploaded_image = st.file_uploader("Image to classify.")
    if uploaded_image is not None:
        col1, col2, col3 = st.columns([1, 1, 1])
        col2.image(uploaded_image, use_column_width=True)

        df_predictions = predict_all(uploaded_image, df_extract["Experiment Name"].to_list())

        st.write(df_predictions)
