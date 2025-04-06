from tsfresh import extract_features
from tsfresh.feature_extraction import EfficientFCParameters
from tsfresh.feature_extraction.settings import from_columns
import pandas as pd


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
