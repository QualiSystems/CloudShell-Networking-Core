from abc import ABCMeta
from abc import abstractmethod


class ConfigurationOperationsInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def save_configuration(self, folder_path, configuration_type, vrf_management_name=None):
        pass

    @abstractmethod
    def restore_configuration(self, path, configuration_type, restore_method, vrf_management_name=None):
        pass

    @abstractmethod
    def orchestration_restore(self, context, saved_artifact_info, custom_params=None):
        pass

    @abstractmethod
    def orchestration_save(self, context, mode="shallow", custom_params=None):
        pass
