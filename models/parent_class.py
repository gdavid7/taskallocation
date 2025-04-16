from abc import ABC, abstractmethod
class Model(ABC):
    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name
    
    def get_embedding(self, text):
        pass
    
    def convert(self, issue: dict) -> list:
        description_embed = self.get_embedding(issue["description"])
        # if issue.get("code"):
        #     code_embed = model.get_embedding(issue["code"])
        #     return [description_embed, code_embed]
        return description_embed

    def compare(self, task1, task2, weight_desc = 0.6, weight_code = 0.4):
        pass