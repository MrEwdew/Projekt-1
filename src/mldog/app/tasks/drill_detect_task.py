import os
import time
import numpy as np
import pandas as pd

from mldog.util.drill_detect.data import (
    convertDrillTimeSeriesToFeatures,
    fcParametersFromFeatureNamesIn,
)
from ..model.task import Task
from ...util.drill.drill_procedure_detector import DrillProcedureDetector
from sklearn.pipeline import Pipeline
import pickle


class DrillDetectTask(Task):
    """
    Drill Detect Task. Detects Drill procedures and forwards the result of the underlying ML Pipeline
    """

    def __init__(
        self,
        model_path: str,
        ttl_max=150,
        window_size=48000,
        active_power=50,
    ):
        """
        Parameters
        ----------
        model_path: str
            Path to the saved model
        ttl_max : int
            The TTL (time-to-live) counter reset value.
        window_size : int
            The number of measurements before and after a detected drill procedure.
        active_power : int
            The power level beyond which the drill is considered active / drilling (and inactive below).

        """
        super().__init__("DrillDetect")
        self.detector = DrillProcedureDetector(ttl_max, window_size, active_power)
        self.started = False

        with open(model_path, "rb") as input_file:
            print(f"Using model at path: {model_path}")
            self.model: Pipeline = pickle.load(input_file)
        self.fcParameters = fcParametersFromFeatureNamesIn(self.model.feature_names_in_)

        print(f"Using features: {self.fcParameters}")

    def process(self, data: np.ndarray) -> None:
        """
        Process new measurement data.

        Measurement data is received in chunks (sequential data portions).
        This method is automatically called by the task thread for each incoming data chunk during an active measurement.
        Any complex / time consuming calculations on measurement data should be performed within this method.

        Parameters
        ----------
        data: ndarray
            The next chunk of measurement data to process.

        Returns
        -------
        None
        """
        
        drill_data = self.detector.update(data)

        if not self.started and self.detector.start_detected:
            self.publishResult("Bohrvorgang gestartet")
            self.started = True

        # check for successful drill procedure detection and publish it accordingly
        if drill_data is not None:
            start = time.time()
            self.started = False
            self.publishResult("Analysiere Bohrvorgang...")
            try:
                self.handleData(drill_data)
                print("dauer: " + f"{(time.time() - start)}")
            except Exception as e:
                print(f"An error occurred:\n{e}")
                self.publishResult(
                    "Etwas ist schiefgelaufen. Starte das Programm bitte neu!"
                )
        

    def handleData(self, data: np.ndarray) -> None:
        """
        feeds the drill data into the ml Pipeline and publishes the result to the App

        Parameters
        ----------
        data: ndarray
            A complete drill procedure

        Returns
        -------
        None
        """
        print("handle finished drill procedure")
        if self.model is None:
            print("No model loaded")
            return

        df = pd.DataFrame(data, columns=["# Audio", "Voltage", "Current"])
        self.publishResult(df)
        features = convertDrillTimeSeriesToFeatures(
            df,
            fcParameters=self.fcParameters,
        )

        features = features[self.model.feature_names_in_]
        result = self.model.predict(features)

        self.publishResult(result[0])
