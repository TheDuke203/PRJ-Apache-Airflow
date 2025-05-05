from abc import ABC, abstractmethod


class Model(ABC):
    
    @abstractmethod
    def run(rows, y_cancelled, y_delay, X):
        pass
