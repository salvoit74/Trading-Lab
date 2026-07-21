from abc import ABC, abstractmethod


class BaseSignal(ABC):

    def __init__(self, db):
        self.db = db

    @abstractmethod
    def calculate(self, symbol, parameters):
        pass
