
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


from typing import List
import numpy as np
from DatabaseFunctions.GatherTrainingData import get_combined_data
from Training.GenericModel import Model
from Training.ModelLightGBM import ModelLightGBM

class TrainModels():
    
    def gather(self):
        input_data = get_combined_data()
    
        def parse_input_data(inputData):
            """
            Output tuple containing two targets and single sample data.
            y_* represents the targets
            X represents the sample data.
            Output of form:
            (y_cancelled, y_delay, X)
            """
            y_cancelled = np.array([data[2] for data in inputData])
            y_delay = np.array([data[1] for data in inputData])
            
            X = []
            for data in inputData:
                departure_station = data[3]
                destination_station = data[4]
                day_of_week = data[6].weekday()
                day_of_year = data[6].timetuple().tm_yday
                seconds_of_day = (data[5].hour * 60   + data[5].minute) * 60
                temperature = data[11]
                weather = data[12]
                wind_speed = data[13]
                X.append([departure_station, destination_station, day_of_week, day_of_year, seconds_of_day,
                        temperature, weather, wind_speed])
        
            return (y_cancelled, y_delay, np.array(X))  
    
        y_cancelled, y_delay, X = parse_input_data(input_data)
        rows = str(len(X)) 
        print("Building on: " + rows + " rows of data")
        return (rows, y_cancelled, y_delay, X)
    
    def __init__(self, models: List[Model]):
        self.models = models
    
    def models_loop(self):
        rows, y_cancelled, y_delay, X = self.gather()
        for model in self.models:
            model.run(rows, y_cancelled, y_delay, X)

def run_general_models():
    
    # All the models to run are created here
    lgbmModel = ModelLightGBM()
    
    # Pass in the models to run as part of our loop
    generalModel = TrainModels([lgbmModel])
    generalModel.models_loop()

def run_custom_models():
    # All the models to run are created here
    lgbmModel = ModelLightGBM()
    
    # Pass in the models to run as part of our loop
    generalModel = TrainModels([lgbmModel])
    generalModel.models_loop()