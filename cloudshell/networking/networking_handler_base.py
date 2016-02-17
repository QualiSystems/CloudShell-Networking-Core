
from abc import ABCMeta
from abc import abstractmethod
from cloudshell.shell.core.handler_base import HandlerBase

class NetworkingHandlerBase(HandlerBase):

    @abstractmethod
    def send_command(self, cmd, expected_str=None, timeout=30):
        pass

    @abstractmethod
    def restore_configuration(self, source_file, clear_config='override'):
        pass

    @abstractmethod
    def backup_configuration(self, destination_host, source_filename):
        pass

    @abstractmethod
    def normalize_output(self, output):
        pass

    @abstractmethod
    def update_firmware(self, remote_host, file_path):
        pass

    @abstractmethod
    def discover_snmp(self):
        pass
