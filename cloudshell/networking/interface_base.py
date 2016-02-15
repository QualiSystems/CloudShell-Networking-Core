__author__ = 'g8y3e'

from abc import ABCMeta

class InterfaceBase:
    __metaclass__ = ABCMeta

    #@abstractmethod
    def get_commands_list(self, **kwargs):
        pass
