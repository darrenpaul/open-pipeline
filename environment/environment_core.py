import os
import sys
import glob
import copy
from pprint import pprint

ROOT_DIR = os.path.dirname(os.path.abspath(__file__).replace(os.sep, "/"))
sys.path.append(ROOT_DIR)
from modules.read_write import op_yaml
from modules.manipulation import op_string
from modules.application import application_object

class Environment:
    def __init__(self, set_envs=True, **kwargs):
        self.setEnvs = set_envs
        self.core_variables = copy.deepcopy(kwargs)
        self.apps = []
        self.configs = {}
        self.applications = []
        self.update_environment_data()
        # self.__check_if_app_available()

    def update_environment_data(self):

        self.__get_platform()
        self.__get_user()
        self.__get_host()
        self.__consume_core_config()
        self.__consume_system_config()
        self.__consume_application_config()
        self.__consume_paths_config()
        self.__consume_miscellaneous_config()
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
        self.core_variables.update({"_script_source": ROOT_DIR})
        _configSource = os.path.join(ROOT_DIR, "configs")
        self.core_variables.update({"_config_source": _configSource})
        _config = op_yaml.read_yaml(path=os.path.join(_configSource, "core.yaml"))
        for k, v in _config["configs"].iteritems():
            self.configs.update({k: op_string.resolve_string(data=self.core_variables, string=v)})
        for k, v in _config["sources"].iteritems():
            self.core_variables.update({k: op_string.resolve_string(data=self.core_variables, string=v)})

    def __consume_system_config(self):
        if "system" in self.configs:
            _config = op_yaml.read_yaml(path=self.configs["system"])
            self.core_variables.update(_config[self.platform])

    def __consume_application_config(self):
        self.__consume_config(config_name="application")
        _applicationConfig = self.configs.get("application")
        if _applicationConfig:
            for k, v in op_yaml.read_yaml(path=self.configs["application"]).items():
                _configPath = op_string.resolve_string(data=self.core_variables, string=v)
                self.configs.update({k: _configPath})
                self.__initialise_application(config_path=_configPath)

    def __consume_paths_config(self):
        config_name = "paths"
        if config_name in self.configs:
            _config = op_yaml.read_yaml(path=self.configs[config_name])
            for k, v in _config.iteritems():
                _configPath = op_string.resolve_string(data=self.core_variables, string=v)
                self.configs.update({k: _configPath})
                self.__consume_template_config(key_name=k)

    def __consume_miscellaneous_config(self):
        config_name = "miscellaneous"
        if config_name in self.configs:
            _config = op_yaml.read_yaml(path=self.configs[config_name])
            for k, v in _config.iteritems():
                _configPath = op_string.resolve_string(data=self.core_variables, string=v)
                self.configs.update({k: _configPath})
                self.__consume_template_config(key_name=k)

    def __consume_template_config(self, key_name):
        if key_name in self.configs:
            _configPath = self.configs.get(key_name)
            for item in op_yaml.read_yaml(path=_configPath):
                for k, v in item.items():
                    _configPath = op_string.resolve_string(data=self.core_variables, string=v)
                    self.core_variables.update({k: _configPath})

    def __consume_config(self, config_name):
        if config_name in self.configs:
            _config = op_yaml.read_yaml(path=self.configs[config_name])
            for k, v in _config.iteritems():
                _configPath = op_string.resolve_string(data=self.core_variables, string=v)
                self.configs.update({k: _configPath})

    def __initialise_application(self, config_path):
        _data = op_yaml.read_yaml(path=config_path)
        application_object.Application(environment=self, config_data=_data)

        #     # Check if application installed
        #     for ver in utils.get_app_version_from_path(path=_directory):
        #         __directory = _directory
        #         _directory = _directory.replace("*", ver)
        #         if os.path.exists(os.path.join(_directory, v)):
        #             # Checks if environment object has application object
        #             if hasattr(self, appname) is False:
        #                 _app = Application(environment=self, appname=appname, directory=__directory)
        #                 if "flags" in _config:
        #                     if self.platform in _config["flags"]:
        #                         setattr(_app, "flags", _config["flags"][self.platform])
        #                 setattr(self, appname, _app)

        #             _app = getattr(self, appname)
        #             _app.products.update({k: v})
        #             if ver not in _app.versions:
        #                 _app.versions.append(ver)
        #                 _app.versions.sort(reverse=True)

        #             if appname not in self.apps:
        #                 self.apps.append(appname)

    def __initialise_application_old(self, appname, config):
        _config = utils.read_yaml(path=config)
        for k, v in _config["product"].iteritems():
            if self.platform == "windows":
                v = os.path.splitext(v)[0]
                v = "{app}.exe".format(app=v)
            _directory = utils.resolve_string(data=self.envs, string=_config["location"][self.platform])
            _config["location"][self.platform] = _directory

            # Check if application installed
            for ver in utils.get_app_version_from_path(path=_directory):
                __directory = _directory
                _directory = _directory.replace("*", ver)
                if os.path.exists(os.path.join(_directory, v)):
                    # Checks if environment object has application object
                    if hasattr(self, appname) is False:
                        _app = Application(environment=self, appname=appname, directory=__directory)
                        if "flags" in _config:
                            if self.platform in _config["flags"]:
                                setattr(_app, "flags", _config["flags"][self.platform])
                        setattr(self, appname, _app)

                    _app = getattr(self, appname)
                    _app.products.update({k: v})
                    if ver not in _app.versions:
                        _app.versions.append(ver)
                        _app.versions.sort(reverse=True)

                    if appname not in self.apps:
                        self.apps.append(appname)



# envObj = Environment(**{"client": "apples"})
# pprint(envObj.core_variables)
# pprint(envObj.configs)
# envObj.maya.launch(product="maya", version="2016")
# print "++++++++++++++++++++++++"
# pprint(envObj.__dict__)
# pprint(envObj.maya.__dict__)

# pprint(envObj.core_variables)
# pprint(envObj.configs)

