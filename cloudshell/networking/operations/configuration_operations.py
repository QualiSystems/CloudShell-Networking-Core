import datetime
import jsonpickle

from abc import abstractmethod
import re

from cloudshell.networking.core.json_request_helper import JsonRequestDeserializer
from cloudshell.networking.networking_utils import UrlParser
from cloudshell.networking.operations.interfaces.configuration_operations_interface import \
    ConfigurationOperationsInterface
from cloudshell.shell.core.context_utils import get_attribute_by_name
from cloudshell.shell.core.interfaces.save_restore import OrchestrationSaveResult, OrchestrationSavedArtifactInfo, \
    OrchestrationSavedArtifact, OrchestrationRestoreRules


def _get_snapshot_time_stamp():
    return datetime.datetime.now()


def set_command_result(result, unpicklable=False):
    """Serializes output as JSON and writes it to console output wrapped with special prefix and suffix

    :param result: Result to return
    :param unpicklable: If True adds JSON can be deserialized as real object.
                        When False will be deserialized as dictionary
    """

    json = jsonpickle.encode(result, unpicklable=unpicklable)
    result_for_output = str(json)  # .replace('[true]', 'true')
    return result_for_output


class ConfigurationOperations(ConfigurationOperationsInterface):
    REQUIRED_SAVE_ATTRIBUTES_LIST = ['resource_name', ('saved_artifact', 'identifier'),
                                     ('saved_artifact', 'artifact_type'), ('saved_artifact', 'server'),
                                     ('restore_rules', 'requires_same_resource')]

    @property
    @abstractmethod
    def logger(self):
        pass

    @property
    @abstractmethod
    def resource_name(self):
        pass

    @property
    @abstractmethod
    def api(self):
        pass

    def orchestration_save(self, mode="shallow", custom_params=None):
        """Handle apply connectivity changes request json, trigger add or remove vlan methods,
        get responce from them and create json response

        :param request: json with all required action to configure or remove vlans from certain port
        :return Serialized DriverResponseRoot to json
        :rtype json
        """

        if custom_params is None or custom_params == '':
            raise Exception('ConfigurationOperations', 'request is None or empty')

        params = JsonRequestDeserializer(jsonpickle.decode(custom_params))

        if not params:
            raise Exception('ConfigurationOperations', 'Deserialized custom_params is None or empty')

        save_params = dict()

        if hasattr(params, 'custom_params'):
            if hasattr(params.custom_params, 'configuration_type'):
                save_params['configuration_type'] = params.custom_params.configuration_type

            if hasattr(params.custom_params, 'folder_path'):
                save_params['folder_path'] = params.custom_params.folder_path
            else:
                save_params['folder_path'] = get_attribute_by_name('Backup Location')
                if not save_params['folder_path']:
                    raise Exception('ConfigurationOperations', 'Folder Path is empty')

            url = UrlParser.parse_url(save_params['folder_path'])
            if UrlParser.SCHEME in url and UrlParser.HOSTNAME in url:
                artifact_type = url[UrlParser.SCHEME]
                server_address = url[UrlParser.HOSTNAME]
            else:
                raise Exception('ConfigurationOperations', 'Cannot retrieve artifact type')

            if hasattr(params.custom_params, 'vrf_management_name'):
                save_params['vrf_management_name'] = params.custom_params.vrf_management_name

        self.logger.info('Action: ', params.__dict__)
        result = self.save(**save_params)

        saved_artifact = OrchestrationSavedArtifact(identifier=result, artifact_type=artifact_type,
                                                    server=server_address, ftp_resource='')

        saved_artifact_info = OrchestrationSavedArtifactInfo(resource_name=self.resource_name,
                                                             created_date=_get_snapshot_time_stamp(),
                                                             restore_rules=self.get_restore_rules(),
                                                             saved_artifact=saved_artifact)
        save_response = OrchestrationSaveResult(saved_artifacts_info=saved_artifact_info)
        self._validate_artifact_info(saved_artifact_info)

        return set_command_result(save_response)

    def orchestration_restore(self, saved_artifact_info, custom_params=None):
        """Handle apply connectivity changes request json, trigger add or remove vlan methods,
        get responce from them and create json response

        :param request: json with all required action to configure or remove vlans from certain port
        :return Serialized DriverResponseRoot to json
        :rtype json
        """

        restore_params = {}
        configuration_type = 'running'

        if saved_artifact_info is None or saved_artifact_info == '':
            raise Exception('ConfigurationOperations', 'saved_artifact_info is None or empty')

        saved_artifact_info = JsonRequestDeserializer(jsonpickle.decode(saved_artifact_info))
        if not hasattr(saved_artifact_info, 'saved_artifacts_info'):
            raise Exception('ConfigurationOperations', 'Saved_artifacts_info is missing')
        saved_config = saved_artifact_info.saved_artifacts_info
        params = ''
        if custom_params:
            params = jsonpickle.decode(custom_params)
            self._validate_custom_params(params)

        self._validate_artifact_info(saved_config)

        if saved_config.restore_rules.requires_same_resource \
                and saved_config.resource_name.lower() != self.resource_name.lower():
            raise Exception('ConfigurationOperations', 'Incompatible resource, expected {}'.format(self.resource_name))

        url = UrlParser.parse_url(saved_config.saved_artifact.identifier)
        url[UrlParser.SCHEME] = saved_config.saved_artifact.artifact_type
        url[UrlParser.HOSTNAME] = saved_config.saved_artifact.server
        if url[UrlParser.SCHEME] == 'ftp' and saved_config.saved_artifact.ftp_resource:
            url[UrlParser.USERNAME] = self._get_resource_attribute(saved_config.saved_artifact.ftp_resource, 'User')
            url[UrlParser.PASSWORD] = self._get_resource_attribute(saved_config.saved_artifact.ftp_resource, 'Password')

        if hasattr(params, 'custom_params'):
            if hasattr(params.custom_params, 'path'):
                restore_params['path'] = params.custom_params.path
            if hasattr(params.custom_params, 'configuration_type'):
                restore_params['configuration_type'] = params.custom_params.configuration_type
            if hasattr(params.custom_params, 'restore_method'):
                restore_params['restore_method'] = params.custom_params.restore_method
            if hasattr(params.custom_params, 'vrf_management_name'):
                restore_params['vrf_management_name'] = params.custom_params.vrf_management_name
        else:
            restore_params['restore_method'] = 'override'
            restore_params['configuration_type'] = 'running'
            if UrlParser.FILENAME in url and url[UrlParser.FILENAME] and 'startup' in url[UrlParser.FILENAME]:
                restore_params['configuration_type'] = 'startup'
            restore_params['vrf_management_name'] = self._get_resource_attribute(self.resource_name,
                                                                                     'VRF Management Name') or ''
        try:
            restore_params['path'] = UrlParser.build_url(**url)
        except Exception as e:
            self.logger.error('Failed to build url: {}'.format(e))
            if 'path' not in restore_params and not restore_params['path']:
                raise Exception('ConfigurationOperations', 'custom_params is None or empty')

        self.restore(**restore_params)

    def _validate_artifact_info(self, saved_config):
        """Validate action from the request json, according to APPLY_CONNECTIVITY_CHANGES_ACTION_REQUIRED_ATTRIBUTE_LIST

        """
        is_fail = False
        fail_attribute = ''
        for class_attribute in self.REQUIRED_SAVE_ATTRIBUTES_LIST:
            if type(class_attribute) is tuple:
                if not hasattr(saved_config, class_attribute[0]):
                    is_fail = True
                    fail_attribute = class_attribute[0]
                if not hasattr(getattr(saved_config, class_attribute[0]), class_attribute[1]):
                    is_fail = True
                    fail_attribute = class_attribute[1]
            else:
                if not hasattr(saved_config, class_attribute):
                    is_fail = True
                    fail_attribute = class_attribute

        if is_fail:
            raise Exception('ConfigurationOperations',
                            'Mandatory field {0} is missing in Saved Artifact Info request json'.format(
                                fail_attribute))

    def _validate_custom_params(self, custom_params):
        if not hasattr(custom_params, 'custom_params'):
            raise Exception('ConfigurationOperations', 'custom_params input is empty')

    def get_restore_rules(self):
        return OrchestrationRestoreRules(True)

    def _get_resource_attribute(self, resource_name, attribute_name):
        """Get resource attribute by provided attribute_name

        :param resource_name: resource name or full name
        :param attribute_name: name of the attribute
        :return: attribute value
        :rtype: string
        """

        try:
            result = self.api.GetAttributeValue(resource_name, attribute_name).Value
        except Exception as e:
            raise Exception(e.message)
        return result

    @abstractmethod
    def save(self, folder_path, configuration_type, vrf_management_name=None):
        pass

    @abstractmethod
    def restore(self, path, configuration_type, restore_method, vrf_management_name=None):
        pass
