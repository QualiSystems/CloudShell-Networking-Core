from abc import ABCMeta
from abc import abstractmethod


class PowerOperationsInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def shutdown(self):
        pass
