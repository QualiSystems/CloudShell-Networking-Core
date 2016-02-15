__author__ = 'CoYe'

import re

from cloudshell.snmp.quali_snmp import QualiSnmp
from cloudshell.core.logger import qs_logger

class HardwarePlatformDetector:
    RESOURCE_DRIVERS_MAP = {}

    def __init__(self, ip, user='', password='', community='',  private_key='', version='2', logger=None):
        self.snmp = None
        self._logger = logger if logger else qs_logger.getQSLogger(handler_name='SNMP_Hardware_Detector')
        #ToDo ask Gal do we really support v1 snmp, according to the fact it has restrictions for loading mib(unclarified)
        if version == '':
            self._logger.info('"SNMP Version" parameter is empty. Use snmp v2 as default.')
            version = '2'
        if '3' in version:
            self.init_snmp_v3(ip, user, password, private_key)
        else:
            self.init_snmp_v2(ip, community)
        self._test_snmp_agent()
        self._logger.info('Snmp handler created. Version {0}'.format(version))

    def init_snmp_v2(self, ip, community):
        """
        Create snmp handler version 2 or 1
        """
        if community == '':
            self._logger.error('"SNMP Read Community" parameter is empty!')
            raise Exception('"SNMP Read Community" parameter is empty!')
        self.snmp = QualiSnmp(ip=ip, community=community, logger=self._logger)

    def init_snmp_v3(self, ip, user, password, private_key):
        """
        Create snmp handler version 3
        """
        if user == '':
            self._logger.error('"SNMP V3 User" parameter is empty')
            raise Exception('"SNMP V3 User" parameter is empty')
        if password == '':
            self._logger.error('"SNMP V3 Password" parameter is empty')
            raise Exception('"SNMP V3 Password" parameter is empty')
        if private_key == '':
            self._logger.error('"SNMP V3 Private Key" parameter is empty')
            raise Exception('"SNMP V3 Private Key" parameter is empty')
        v3_user = {'userName': user, 'authKey': password, 'privKey': private_key}
        self.snmp = QualiSnmp(ip=ip, v3_user=v3_user)

    def _test_snmp_agent(self):
        """
        Validate snmp agent and connectivity attributes, raise Exception if snmp agent is invalid
        """
        try:
            self.snmp.get(('SNMPv2-MIB', 'sysName', '0'))
        except Exception as e:
            self._logger.error('Snmp agent validation failed')
            self._logger.error(e.message)
            raise Exception('Snmp attributes or host IP is not valid\n{0}'.format(e.message))

    def _detect_hardware_platform(self):
        """
        Detect target device platform
        :return: handler name
        :rtype: string
        """
        handler = None
        hardware_info = self.snmp.get(('SNMPv2-MIB', 'sysObjectID', '0')).values()[0]

        match_object = re.search(r'^SNMPv2-SMI::enterprises\.(?P<vendor>\d+)(\.\d)+\.(?P<model>\d+$)', hardware_info)
        if match_object is None:
            match_object = re.search(r'1\.3\.6\.1\.4\.1\.(?P<vendor>\d+)(\.\d)+\.(?P<model>\d+$)', hardware_info)
        if match_object is not None:
            result = match_object.groupdict()
            if result['vendor'] and result['vendor'] in self.RESOURCE_DRIVERS_MAP:
                if result['model'] in self.RESOURCE_DRIVERS_MAP[result['vendor']]:
                    handler = self.RESOURCE_DRIVERS_MAP[result['vendor']][result['model']]
        if handler:
            self._logger.info('Detected platform: {0}'.format(handler))
        return handler