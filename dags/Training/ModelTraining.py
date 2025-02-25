import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from DatabaseFunctions.GatherTrainingData import get_combined_data

import numpy as np
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from sklearn.metrics import accuracy_score
from DatabaseFunctions.ModelResults import push_model_results
from datetime import datetime
from pathlib import Path
'''
Example of data coming from server
(44443, 0, False, 97372160, 25562584, datetime.time(21, 5), datetime.date(2025, 2, 8), 7853, 44443,
1, 1, Decimal('277.60'), 803, 2, datetime.datetime(2025, 2, 8, 21, 0), 97372160)
'''


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
    

def train_model_from_database():
    input_data = get_combined_data()
    y_cancelled, y_delay, X = parse_input_data(input_data)
    rows = str(len(X)) 
    print("Building on: " + rows + " rows of data")
    
    clf_model, accuracy, true_ratio = test_train_cancelled_classification(X,y_cancelled)
    clf_model.booster_.save_model(Path(f'models/lgb_classifier_{datetime.now().strftime("%Y-%m-%d")}.txt'))
    
    reg_model, r_squared = test_train_delay_regression(X, y_delay)
    reg_model.booster_.save_model(Path(f'models/lgb_regressor_{datetime.now().strftime("%Y-%m-%d")}.txt'))

    print("Regresssion: R_squared result is: "+ str(r_squared))
    print("Classification: Accuracy is: " + str(accuracy))
    print("Classification: True ratio is: " + str(true_ratio))
    
    push_model_results(rows, accuracy, r_squared.item(), true_ratio)   



def test_train_cancelled_classification(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
    clf = lgb.LGBMClassifier(random_state=0, is_unbalance=True)
    clf.fit(X_train, y_train)
    
    y_pred=clf.predict(X_test)    
    return (clf, accuracy_score(y_test, y_pred) ,test_false_positives(y_test, y_pred))


def test_false_positives(y_test, y_pred):
    total = np.count_nonzero(y_test)
    correct = 0
    for i in range(len(y_test)):
        if y_test[i] == 1 and y_pred[i] == 1:
            correct += 1
    
    return str(correct / total)

def test_train_delay_regression(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
    model = lgb.LGBMRegressor()
    model.fit(X_train, y_train)
    
    y_pred=model.predict(X_test)
    return (model, r_square_scratch(y_test, y_pred))
    
def r_square_scratch(true, predicted):
    # substract each predicted value from each true
    residuals = [a - b for a, b in zip(true, predicted)]
    # calculate the sum of squared differences between predicted and true
    mss = sum([i**2 for i in residuals])
    # calculate the mean true value
    mean_true = (sum(true))/len(true)
    # calculate the sum of squared differences of each true value minus the mean true value
    tss = sum([(i-mean_true)**2 for i in true])
    # calculate final r2 value
    return 1-(mss/tss)