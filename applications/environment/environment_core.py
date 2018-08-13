import os
import sys
import glob
from pprint import pprint

ROOT_DIR = os.path.abspath(os.path.join(__file__ , "../../../")).replace(os.sep, "/")

sys.path.append(ROOT_DIR)
from engines.read_write import op_yaml

class Environment:
    def __init__(self, set_envs=True, **kwargs):
        self.setEnvs = set_envs
        self.core_variables = kwargs
        # self.apps = []
        # self.configs = {}
        # self.applications = []
        # self.update_environment_data()
        # self.__check_if_app_available()

    def update_environment_data(self):
        if self.core_variables:
            self.__get_platform()
            self.__get_user()
            self.__get_host()
            self.__consume_core_config()
            # self._consume_system_config()
            # self._consume_application_config()
            # self._consume_paths_config()
            # self._consume_context_config()
            # self._consume_miscellaneous()
            # if self.setEnvs:
            #     os.environ.update(self.core_variables)

    def __get_platform(self):
        try:
            import platform
            self.platform = platform.system().lower()
            self.core_variables.update({"os": self.platform})
        except:
            raise Exception("Failed to determine platform")

    def __get_user(self):
        try:
            import getpass
            self.user = getpass.getuser()
            self.core_variables.update({"user": self.user})
        except:
            raise Exception("Failed to get user")

    def __get_host(self):
        try:
            import socket
            self.hostname = socket.gethostname()
            self.core_variables.update({"hostname": self.hostname})
        except:
            raise Exception("Failed to get hostname")

    def __consume_core_config(self):
        import copy
        self.core_variables.update({"_script_source": os.path.dirname(os.path.dirname(ROOTDIR))})
        _configsource = os.path.join(ROOTDIR, "configs")
        self.core_variables.update({"_config_source": _configsource})
        _config = utils.read_yaml(path=os.path.join(_configsource, "core.yaml"))
        for k, v in _config["configs"].iteritems():
            self.configs.update({k: utils.resolve_string(data=self.core_variables, string=v)})
        for k, v in _config["sources"].iteritems():
            self.core_variables.update({k: utils.resolve_string(data=self.core_variables, string=v)})
