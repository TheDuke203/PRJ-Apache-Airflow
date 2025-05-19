import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


from sklearn.metrics import recall_score, accuracy_score, r2_score
from sklearn.model_selection import train_test_split
from Training.GenericModel import Model
import autosklearn.classification
import autosklearn.regression
from datetime import datetime
from pathlib import Path



class ModelAutoLM(Model):
    
    def run(self, rows, y_cancelled, y_delay, X):
        clf_model, accuracy, true_ratio = ModelAutoLM.build_test_classification(X,y_cancelled)
        # clf_model.booster_.save_model(Path(f'models/lgb_classifier_{datetime.now().strftime("%Y-%m-%d")}.txt'))
        
        reg_model, r_squared = ModelAutoLM.build_test_regression(X, y_delay)
        # reg_model.booster_.save_model(Path(f'models/lgb_regressor_{datetime.now().strftime("%Y-%m-%d")}.txt'))

        print("Regresssion: R_squared result is: "+ str(r_squared))
        print("Classification: Accuracy is: " + str(accuracy))
        print("Classification: True ratio is: " + str(true_ratio))
        
        # push_model_results(rows, accuracy, r_squared, true_ratio) 
    
    def build_test_classification(X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
        cls = autosklearn.classification.AutoSklearnClassifier()
        cls.fit(X_train, y_train)
        
        y_pred=cls.predict(X_test)    
        return (cls, accuracy_score(y_test, y_pred), recall_score(y_test, y_pred))

    def build_test_regression(X,y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
        model = autosklearn.regression.AutoSklearnRegressor()
        model.fit(X_train, y_train)
        
        y_pred=model.predict(X_test)
        return (model, r2_score(y_test, y_pred))