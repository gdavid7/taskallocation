from abc import ABC, abstractmethod
class Model(ABC):
    def compare(self, task1, task2, weight_desc = 0.6, weight_code = 0.4):
        pass
    def __init__(self, name):
        self._name = name
    def name(self):
        return self._name
    
