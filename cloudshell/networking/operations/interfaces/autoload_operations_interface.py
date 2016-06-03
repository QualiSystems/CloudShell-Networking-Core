from abc import ABCMeta
from abc import abstractmethod


class AutoloadOperationsInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def discover(self):
        pass
