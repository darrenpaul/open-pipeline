import os
from pprint import pprint

from modules.application import tools as app_tools
from modules.application import start_up as app_start_up
from modules.read_write import op_yaml
from modules.manipulation import op_string

class Application:
    def __init__(self, environment, config_data):
        self.environment = environment
        self.config_data = config_data
        self.appname = ""
        self.executable = ""
        self.products = {}
        self.versions = []
        self.update_application()

    def update_application(self):
        for base, product in self.config_data["product"].items():
            _executable = app_tools.set_executable(platform=self.environment.platform, application_name=product)
            _directory = op_string.resolve_string(data=self.environment.core_variables, string=self.config_data["location"][self.environment.platform])

            self.executable = os.path.join(_directory, _executable).replace(os.sep, "/")
            self.config_data["location"][self.environment.platform] = _directory
            self.versions = app_tools.get_all_application_versions(application_path=os.path.join(_directory, _executable))
            self._set_flags(base_name=base)

            self.products.update({base: product})

            if base not in self.environment.apps:
                self.environment.apps.append(base)
            self.appname = base

    def launch(self, product, version=""):
        self.__check_version(version=version)

        self.environment.core_variables.update({"appname": self.appname, "appversion": self.version})

        self.__run_app_startup()
        
        if "working_directory" in self.environment.core_variables:
            os.chdir(self.environment.core_variables["working_directory"])

        print "Launching {app}".format(app=self.appname)
        self.__create_launch_command(product=product)
        print self.__create_launch_command(product=product)
        os.system(self.__create_launch_command(product=product))

        pprint(self.environment.core_variables)

    def _set_flags(self, base_name):
        if hasattr(self.environment, base_name) is False:
            if "flags" in self.config_data:
                if self.environment.platform in self.config_data["flags"]:
                    self.flags = self.config_data["flags"][self.environment.platform]
            setattr(self.environment, base_name, self)
            
    def __run_app_startup(self):
        app_start_up.setup_application(self.environment)

    def __check_version(self, version):
        if version is "":
            version = self.versions[0]
        self.version = version

    def __check_flags(self):
        _resolved = []
        if hasattr(self, "flags"):
            for f in self.flags:
                _resolved.append(utils.resolve_string(data=self.environment.core_variables, string=f))
            if len(_resolved) > 0:
                return " ".join(_resolved)
            return " ".join(self.flags)
        return ""

    def __create_launch_command(self, product):
        _executable = self.executable.replace("*", self.version)
        _flags = self.__check_flags()

        if app_tools.check_if_resolved(string=_flags) is False:
            _flags = ""

        _command = "{cmd} '{exe}' {flags}".format(cmd=self.environment.core_variables["_launch"], exe=_executable, flags=_flags)
        return _command
