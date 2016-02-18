import json

from cloudshell.networking.networking_resource_driver_interface import NetworkingResourceDriverInterface
from cloudshell.shell.core.driver_builder_wrapper import BaseResourceDriver, DriverFunction
from cloudshell.shell.core.handler_factory import HandlerFactory
from cloudshell.core.logger import qs_logger
from cloudshell.networking.platform_detector.hardware_platform_detector import HardwarePlatformDetector


class networking_generic_resource_driver(BaseResourceDriver, NetworkingResourceDriverInterface):
    REQUIRED_RESORCE_ATTRIBUTES = {
        "resource": ["ResourceAddress", "User", "Password", "Enable Password", "Console Server IP Address",
                     "Console User", "Console Password", "Console Port", "Connection Type",
                     "SNMP Version", "SNMP Read Community", "SNMP V3 User", "SNMP V3 Password",
                     "SNMP V3 Private Key"]}

    @staticmethod
    def create_snmp_helper(host, json_object_resource, logger):

        snmp_helper = None
        if 'SNMP V3 User' in json_object_resource.keys():
            snmp_helper = HardwarePlatformDetector(ip=host,
                                                   user=json_object_resource['SNMP V3 User'],
                                                   password=json_object_resource['SNMP V3 Password'],
                                                   community=json_object_resource['SNMP Read Community'],
                                                   version=json_object_resource['SNMP Version'],
                                                   private_key=json_object_resource['SNMP V3 Private Key'],
                                                   logger=logger)
        return snmp_helper

    def __detect_hardware_platform(self, snmp_handler):

        if snmp_handler:
            self.temp_snmp_handler = snmp_handler.snmp
            return snmp_handler._detect_hardware_platform()
        return None

    def __check_for_attributes_changes(self, matrixJSON):
        """Verify if resource and/re reservation details changed, update handler accordingly

        :param matrixJSON:
        :return:
        """
        json_object = json.loads(matrixJSON)
        self._resource_handler._logger.info('Self MATRIX = {0}'.format(self._json_matrix))
        self._resource_handler._logger.info('NEW MATRIX = {0}'.format(json_object))

        merged_matrix = {}
        for matrix_key in json_object.keys():
            matrix = json_object[matrix_key]

            if not matrix in self._json_matrix.keys():
                self._json_matrix[matrix_key] = matrix
                self.Init(matrixJSON)
                return

            for key, val in matrix.iteritems():
                if not key in self._json_matrix[matrix_key].keys():
                    # skip extra parameters, compare only existing keys
                    pass
                elif self._json_matrix[matrix_key][key] != matrix[key]:
                    if key in ['User', 'Password', 'ResourceAddress', 'CLI Connection Type', 'ReservationId']:
                        # Init handler again
                        self.Init(matrixJSON)
                        return

                    elif key in ['SNMP V3 User', 'SNMP V3 Password', 'SNMP Read Community', 'SNMP Version',
                                 'SNMP V3 Private Key']:
                        # create new SNMP handler
                        current_logger = self._resource_handler._logger

                        merged_matrix[matrix_key] = self._json_matrix[matrix_key]
                        merged_matrix.update(json_object)

                        handler_params = self.get_handler_parameters_from_json(merged_matrix)
                        snmp_helper = networking_generic_resource_driver.create_snmp_helper(handler_params['host'],
                                                                                            json_object['resource'],
                                                                                            current_logger)
                        self._resource_handler._snmp_handler = snmp_helper.snmp

        self._json_matrix = merged_matrix

    def get_handler_parameters_from_json(self, json_object):

        logger_params = {'handler_name': self.resource_name,
                         'reservation_details': json_object['reservation']}
        handler_params = {}

        if 'User' in json_object['resource']:
            handler_params['username'] = json_object['resource']['User'].encode('ascii', errors='backslashreplace')
            handler_params['password'] = json_object['resource']['Password'].encode('ascii', errors='backslashreplace')
            handler_params['enable_password'] = json_object['resource']['Enable Password'].encode('ascii',
                                                                                                  errors='backslashreplace')
            handler_params['console_server_ip'] = json_object['resource']['Console Server IP Address'].encode('ascii',
                                                                                                              errors='backslashreplace')
            handler_params['console_server_user'] = json_object['resource']['Console User'].encode('ascii',
                                                                                                   errors='backslashreplace')
            handler_params['console_server_password'] = json_object['resource']['Console Password'].encode('ascii',
                                                                                                           errors='backslashreplace')
            handler_params['console_port'] = json_object['resource']['Console Port'].encode('ascii',
                                                                                            errors='backslashreplace')
            handler_params['session_handler_name'] = json_object['resource']['CLI Connection Type'].encode('ascii',
                                                                                                           errors='backslashreplace')
            if len(handler_params['session_handler_name']) == 0:
                handler_params['session_handler_name'] = 'auto'
        handler_params['logger_params'] = logger_params

        address_elements = json_object['resource']['ResourceAddress'].encode('ascii', errors='backslashreplace').split(
            ':')
        handler_params['host'] = address_elements[0]
        if len(address_elements) > 1:
            handler_params['port'] = address_elements[1]

        return handler_params

    @DriverFunction(extraMatrixRows=REQUIRED_RESORCE_ATTRIBUTES)
    def Init(self, matrixJSON):
        detected_platform_name = None
        json_object = json.loads(matrixJSON)
        self._json_matrix = json_object
        self.resource_name = 'generic_resource'
        if not self.handler_name:
            self.handler_name = 'generic_driver'

        self.temp_snmp_handler = None

        # set initial reservation ID to 'Autoload' will be used if not other provided.
        self.reservation_id = 'Autoload'

        if 'ResourceName' in json_object['resource'] and not json_object['resource']['ResourceName'] is None:
            self.resource_name = json_object['resource']['ResourceName']

        if 'reservation' in json_object:
            if 'ReservationId' in json_object['reservation'] and \
                    not json_object['reservation']['ReservationId'] is None:
                self.reservation_id = json_object['reservation']['ReservationId']
        else:
            json_object['reservation'] = {}
            json_object['reservation']['ReservationId'] = self.reservation_id

        handler_params = self.get_handler_parameters_from_json(json_object)
        if 'Filename' in json_object['resource'] and json_object['resource']['Filename'] != '':
            handler_params['session_handler_name'] = 'file'
            handler_params['filename'] = json_object['resource']['Filename']
            if 'HandlerName' in json_object['resource'] and json_object['resource']['HandlerName'] != '':
                detected_platform_name = json_object['resource']['HandlerName']
        else:
            driver_logger = HandlerFactory.get_logger(self.handler_name, logger_params=handler_params['logger_params'])
            handler_params['logger'] = driver_logger

            tmp_snmp_handler = networking_generic_resource_driver.create_snmp_helper(handler_params['host'],
                                                                                     json_object['resource'],
                                                                                     driver_logger)
            detected_platform_name = self.__detect_hardware_platform(tmp_snmp_handler)

        if detected_platform_name:
            self.handler_name = detected_platform_name

        self._resource_handler = HandlerFactory.create_handler(self.handler_name, **handler_params)
        self._resource_handler._logger.info('Created resource handle {0}'.format(self.handler_name.upper()))

        self._resource_handler.set_parameters(json_object)

        if self.temp_snmp_handler:
            self._resource_handler._snmp_handler = self.temp_snmp_handler

        log_path = qs_logger.get_log_path(self._resource_handler._logger)
        if log_path:
            return 'Log Path: {0}'.format(log_path)
            # return 'Log Path: {0}'.format(self._resource_handler._logger.handlers[0].baseFilename)

    @DriverFunction(alias='Get Inventory', extraMatrixRows=REQUIRED_RESORCE_ATTRIBUTES)
    def GetInventory(self, matrixJSON):
        """
        Return device structure with all standard attributes
        :return: result
        :rtype: string
        """
        self.__check_for_attributes_changes(matrixJSON)
        result = self._resource_handler.discover_snmp()
        return self._resource_handler.normalize_output(result)

    @DriverFunction(alias='Update Firmware', extraMatrixRows=REQUIRED_RESORCE_ATTRIBUTES)
    def UpdateFirmware(self, matrixJSON, remote_host, file_path):
        """
        Upload and updates firmware on the resource
        :return: result
        :rtype: string
        """
        self.__check_for_attributes_changes(matrixJSON)
        result_str = self._resource_handler.update_firmware(remote_host=remote_host, file_path=file_path)
        self._resource_handler.disconnect()
        return self._resource_handler.normalize_output(result_str)

    @DriverFunction(alias='Save', extraMatrixRows=REQUIRED_RESORCE_ATTRIBUTES)
    def Save(self, matrixJSON, folder_path, configuration_type):
        """
        Backup configuration
        :return: success string with saved file name
        :rtype: string
        """

        self.__check_for_attributes_changes(matrixJSON)
        result_str = self._resource_handler.backup_configuration(destination_host=folder_path,
                                                                 source_filename=configuration_type)
        return self._resource_handler.normalize_output(result_str)

    @DriverFunction(alias='Restore', extraMatrixRows=REQUIRED_RESORCE_ATTRIBUTES)
    def Restore(self, matrixJSON, path, restore_method='Override'):
        """
        Restore configuration
        :return: success string
        :rtype: string
        """
        self.__check_for_attributes_changes(matrixJSON)
        result_str = self._resource_handler.restore_configuration(source_file=path, clear_config=restore_method)
        return self._resource_handler.normalize_output(result_str)

    @DriverFunction(alias='Send Command', extraMatrixRows=REQUIRED_RESORCE_ATTRIBUTES)
    def SendCustomCommand(self, matrixJSON, command):
        """
        Send custom command
        :return: result
        :rtype: string
        """
        self.__check_for_attributes_changes(matrixJSON)
        result_str = self._resource_handler.send_command(cmd=command)
        return self._resource_handler.normalize_output(result_str)

    @DriverFunction(alias='Add Vlan', category='Hidden Commands', extraMatrixRows=REQUIRED_RESORCE_ATTRIBUTES)
    def Add_VLAN(self, matrixJSON, ports, vlan_range, switchport_type, additional_info):
        """
        Assign vlan or vlan range to the certain interface
        :return: result
        :rtype: string
        """
        self.__check_for_attributes_changes(matrixJSON)
        result_str = self._resource_handler.configure_vlan(port_list=ports,
                                                           vlan_range=vlan_range.replace(' ', ''),
                                                           switchport_type=switchport_type,
                                                           additional_info=additional_info, remove=False)
        return self._resource_handler.normalize_output(result_str)

    @DriverFunction(alias='Remove Vlan', category='Hidden Commands', extraMatrixRows=REQUIRED_RESORCE_ATTRIBUTES)
    def Remove_VLAN(self, matrixJSON, ports, vlan_range, switchport_type, additional_info):
        """
        Remove vlan or vlan range from the certain interface
        :return: result
        :rtype: string
        """
        self.__check_for_attributes_changes(matrixJSON)
        result_str = self._resource_handler.configure_vlan(port_list=ports,
                                                           vlan_range=vlan_range, switchport_type=switchport_type,
                                                           additional_info=additional_info, remove=True)
        return self._resource_handler.normalize_output(result_str)

    @DriverFunction(alias='Send Config Command', category='Hidden Commands',
                    extraMatrixRows=REQUIRED_RESORCE_ATTRIBUTES)
    def SendCustomConfigCommand(self, matrixJSON, command):
        self.__check_for_attributes_changes(matrixJSON)
        result_str = self._resource_handler.sendConfigCommand(cmd=command)
        return self._resource_handler.normalize_output(result_str)

    @DriverFunction(alias='Reset Driver', extraMatrixRows=REQUIRED_RESORCE_ATTRIBUTES)
    def ResetDriver(self, matrix_json):
        self.Init(matrix_json)
        return 'Driver reset completed'

    def Shutdown(self):
        pass
