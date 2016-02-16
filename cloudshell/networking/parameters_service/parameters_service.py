__author__ = 'g8y3e'

import re

class ParametersService:
    @staticmethod
    def get_validate_list(command_tamplate, properties_list):
        validate_result = ParametersService._validate(properties_list, command_tamplate.getReStringList())
        if validate_result[0]:
            return command_tamplate.getCommand(*properties_list)
        else:
            raise Exception(command_tamplate.getErrorByIndex(validate_result[1]))

    @staticmethod
    def _validate(properties_list, re_string_list):
        if len(properties_list) != len(re_string_list):
            return 'Need ' + str(len(re_string_list)) + ' parameters, but you sended - ' + \
                   str(len(properties_list));

        if len(properties_list) == 0:
            return (True, -1)

        for index in range(0, len(properties_list)):
            if hasattr(re_string_list[index], '__call__'):
                if not re_string_list[index](properties_list[index]):
                    return (False, index)
            elif re.match(re_string_list[index], properties_list[index]) == None:
                return (False, index)

        return (True, -1)