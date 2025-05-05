import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


from Training.GenericModel import Model
import numpy as np
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from sklearn.metrics import accuracy_score, recall_score, r2_score
from DatabaseFunctions.ModelResults import push_model_results
from datetime import datetime
from pathlib import Path
'''
Example of data coming from server
(44443, 0, False, 97372160, 25562584, datetime.time(21, 5), datetime.date(2025, 2, 8), 7853, 44443,
1, 1, Decimal('277.60'), 803, 2, datetime.datetime(2025, 2, 8, 21, 0), 97372160)
'''

class ModelLightGBM(Model):
    
    def run(self, rows, y_cancelled, y_delay, X):
        
        clf_model, accuracy, true_ratio = ModelLightGBM.test_train_cancelled_classification(X,y_cancelled)
        clf_model.booster_.save_model(Path(f'models/lgb_classifier_{datetime.now().strftime("%Y-%m-%d")}.txt'))
        
        reg_model, r_squared = ModelLightGBM.test_train_delay_regression(X, y_delay)
        reg_model.booster_.save_model(Path(f'models/lgb_regressor_{datetime.now().strftime("%Y-%m-%d")}.txt'))

        print("Regresssion: R_squared result is: "+ str(r_squared))
        print("Classification: Accuracy is: " + str(accuracy))
        print("Classification: True ratio is: " + str(true_ratio))
        
        push_model_results(rows, accuracy, r_squared, true_ratio)   


    def test_train_cancelled_classification(X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
        clf = lgb.LGBMClassifier(random_state=0, is_unbalance=True)
        clf.fit(X_train, y_train)
        
        y_pred=clf.predict(X_test)    
        return (clf, accuracy_score(y_test, y_pred), recall_score(y_test, y_pred))

    def test_train_delay_regression(X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
        model = lgb.LGBMRegressor()
        model.fit(X_train, y_train)
        
        y_pred=model.predict(X_test)
        return (model, r2_score(y_test, y_pred))