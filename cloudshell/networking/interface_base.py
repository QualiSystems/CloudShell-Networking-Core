__author__ = 'g8y3e'

from abc import ABCMeta
from abc import abstractmethod

class InterfaceBase:
    __metaclass__ = ABCMeta

	@abstractmethod
    def getCommandsList(self, **kwargs):
		pass