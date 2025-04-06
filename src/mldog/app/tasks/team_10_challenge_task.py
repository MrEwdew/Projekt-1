import numpy as np
import pandas as pd
from tsfresh import extract_features
from tsfresh.feature_extraction import EfficientFCParameters
from tsfresh.feature_extraction.settings import from_columns
import pandas as pd
from ..model.challenge_task import ChallengeTask
from sklearn.pipeline import Pipeline
import pickle
import os


class Team10ChallengeTask(ChallengeTask):
    """
    Simple challenge task class example.
    """

    def __init__(self):
        """
        Construct a new example challenge task instance.
        """
        super().__init__("Team 10")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_name = "team_10_challenge_model.pkl"
        file_path = os.path.join(script_dir, model_name)
        with open(file_path, "rb") as input_file:
            self.model: Pipeline = pickle.load(input_file)
        self.fcParameters = fcParametersFromFeatureNamesIn(self.model.feature_names_in_)

    def predict(self, drill_data: np.ndarray) -> str:
        """
        Classify new drill procedure data.

        This method performs a classification of the provided drill procedure data.

        Parameters
        ----------
        drill_data: ndarray
            The data of a completed drill procedure.

        Returns
        -------
        classification_result : str
            The predicted class (e.g. 'holz-span', etc.).
        """
        try:
            df = pd.DataFrame(drill_data, columns=["# Audio", "Voltage", "Current"])
            features = convertDrillTimeSeriesToFeatures(
                df,
                fcParameters=self.fcParameters,
            )

            features = features[self.model.feature_names_in_]
            result = self.model.predict(features)
            material = result[0]

            return material
        except:
            # default value in case of an error
            return "metall-alu"


def convertDrillTimeSeriesToFeatures(df, columnId=None, fcParameters=None, n_jobs=0):
    """
    Konvertiert einen Bohrvohrgang mittels tsfresh in ausgewählte Features
    columnID: Dataframe spalte die als ID gilt, falls None wird automatisch eine erstell
    fcParameters: Die Features die tsfresh berechnen soll, standardmässig EfficientFcParameters
    """
    if fcParameters is None:
        fcParameters = EfficientFCParameters()

    if columnId == None:
        columnId = "ID"
        df["ID"] = 1

    if is_nested_dict(fcParameters):
        extracted_features = extract_features(
            df, column_id=columnId, kind_to_fc_parameters=fcParameters, n_jobs=n_jobs
        )
    else:
        extracted_features = extract_features(
            df, column_id=columnId, default_fc_parameters=fcParameters, n_jobs=n_jobs
        )

    return extracted_features


def is_nested_dict(var):
    return isinstance(var, dict) and any(isinstance(v, dict) for v in var.values())


def fcParametersFromFeatureNamesIn(features: list[str]) -> dict[str, any]:
    """
    Erstellt die richtige fcParameter für eine liste an gegeben tsfeatures
    """
    df = pd.DataFrame(data=None, columns=features)
    return from_columns(df)
