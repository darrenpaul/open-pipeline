import os
import sys
import glob
from pprint import pprint

ROOTDIR = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, "/")
sys.path.append(os.path.dirname(ROOTDIR))
from utils import utils


class Environment:
    def __init__(self, set_envs=True, **kwargs):
        self.setEnvs = set_envs
        self.envs = kwargs
        self.apps = []
        self.configs = {}
        self.applications = []
        self.update_environment()
        self.__check_if_app_available()

    def update_environment(self):
        if self.envs:
            self._get_platform()
            self._get_user()
            self._get_host()
            self._consume_core_config()
            self._consume_system_config()
            self._consume_application_config()
            self._consume_paths_config()
            self._consume_context_config()
            self._consume_miscellaneous()
            if self.setEnvs:
                os.environ.update(self.envs)


    def build_project(self):
        _config = utils.read_yaml(path=self.configs["context"])
        for i in _config:
            for k, v in i.iteritems():
                _path = utils.resolve_string(data=self.envs, string=v)
                if _check_if_resolved(string=_path):
                    self.envs.update({k: _path})
                    utils.make_directory(path=_path)

    def get_applications(self):
        import collections
        from operator import itemgetter

        _data = collections.OrderedDict()
        for app in self.apps:
            if hasattr(self, app):
                for product in getattr(self, app).products.keys():
                    _appname = app
                    if app != product:
                        _appname = "{app} {product}".format(app=app, product=product)
                    _data.update({_appname: getattr(self, app).versions})

        _data = collections.OrderedDict(sorted(_data.items(), key=itemgetter(1), reverse=True))
        return _data

    def launch(self, product, version=""):
        if " " in product:
            product = product.split(" ")[1]
        appname = None
        for app in self.apps:
            if hasattr(self, app):
                if product in getattr(self, app).products.keys():
                    appname = getattr(self, app).appname
        if appname and hasattr(self, appname):
            getattr(self, appname).launch(product=product, version=version)

    def add_vars_to_system_environment(self):
        os.environ.update(self.envs)

    def add_paths_to_sys_path(self):
        for k, v in self.envs.iteritems():
            if os.path.exists(v):
                if v not in sys.path:
                    sys.path.append(v)

    def list_working_users(self):
        if "working_app" in self.envs:
            return os.listdir(self.envs["working_app"])

    def list_working_scenes(self, user):
        _ext = [".ma", ".mb", ".hip"]
        _files = []
        if "working_user" in self.envs:
            for ext in _ext:
                _files = _files + glob.glob(os.path.join(self.envs["working_app"], user, "*{ext}".format(ext=ext)))
                _files = _files + glob.glob(os.path.join(self.envs["working_app"], user, "*", "*{ext}".format(ext=ext)))

        _unresolved = []
        _working_app = self.envs["working_app"].replace(os.sep, "/")
        for f in _files:
            f = f.replace(os.sep, "/")
            f = f.replace(_working_app, "{working_app}")
            _unresolved.append(f)

        return _unresolved

    def _get_platform(self):
        try:
            import platform
            self.platform = platform.system().lower()
            self.envs.update({"os": self.platform})
        except:
            raise Exception("Failed to determine platform")

    def _get_user(self):
        try:
            # Get User
            import getpass
            self.user = getpass.getuser()
            self.envs.update({"user": self.user})
        except:
            raise Exception("Failed to get user")

    def _get_host(self):
        try:
            # Get Hostname
            import socket
            self.hostname = socket.gethostname()
            self.envs.update({"hostname": self.hostname})
        except:
            raise Exception("Failed to get hostname")

    def _consume_core_config(self):
        import copy
        self.envs.update({"_script_source": os.path.dirname(os.path.dirname(ROOTDIR))})
        _configsource = os.path.join(ROOTDIR, "configs")
        self.envs.update({"_config_source": _configsource})
        _config = utils.read_yaml(path=os.path.join(_configsource, "core.yaml"))
        for k, v in _config["configs"].iteritems():
            self.configs.update({k: utils.resolve_string(data=self.envs, string=v)})
        for k, v in _config["sources"].iteritems():
            self.envs.update({k: utils.resolve_string(data=self.envs, string=v)})

    def _consume_system_config(self):
        if "system" in self.configs:
            _config = utils.read_yaml(path=self.configs["system"])
            self.envs.update(_config[self.platform])

    def _consume_application_config(self):
        if "application" in self.configs:
            _config = utils.read_yaml(path=self.configs["application"])
            for k, v in _config.iteritems():
                _config = utils.resolve_string(data=self.envs, string=v)
                self.configs.update({k: _config})
                self._initialise_application(appname=k, config=_config)

    def _consume_paths_config(self):
        if "paths" in self.configs:
            _config = utils.read_yaml(path=self.configs["paths"])
            for k, v in _config.iteritems():
                _config = utils.resolve_string(data=self.envs, string=v)
                self.configs.update({k: _config})
                # self._initialise_application(appname=k, config=_config)

    def _consume_context_config(self):
        if "context" in self.configs:
            _config = utils.read_yaml(path=self.configs["context"])
            for i in _config:
                for k, v in i.iteritems():
                    _config = utils.resolve_string(data=self.envs, string=v)
                    self.envs.update({k: _config})
    
    def _consume_plugins_config(self):
        if "context" in self.configs:
            _config = utils.read_yaml(path=self.configs["context"])
            for i in _config:
                for k, v in i.iteritems():
                    _config = utils.resolve_string(data=self.envs, string=v)
                    self.envs.update({k: _config})

    def _consume_miscellaneous(self):
        if "miscellaneous" in self.configs:
            for cfg in os.listdir(self.configs["miscellaneous"]):
                _config = utils.read_yaml(path=os.path.join(self.configs["miscellaneous"], cfg))
                for k, v in _config.iteritems():
                    self.envs.update({k: utils.resolve_string(data=self.envs, string=v)})

    def _initialise_application(self, appname, config):
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

    def __check_if_app_available(self):
        if "product" in self.envs:
            self.launch(product=self.envs["product"])


class Application:
    def __init__(self, environment, appname, directory):
        self.appname = appname
        self.environment = environment
        self.directory = directory
        self.products = {}
        self.versions = []

    def launch(self, product, version=""):
        self.__check_version(version=version)

        self.environment.envs.update({"appname": self.appname, "appversion": self.version})
        self.environment.build_project()

        self._run_app_startup()
        os.chdir(self.environment.envs["working_user"])

        print "Launching {app}".format(app=self.appname)
        self.__create_launch_command(product=product)
        os.system(self.__create_launch_command(product=product))

        pprint(self.environment.envs)

    def _run_app_startup(self):
        import application_startup
        application_startup.setup_application(self.environment)

    def __check_version(self, version):
        if version is "":
            version = self.versions[0]
        self.version = version

    def __check_flags(self):
        _resolved = []
        if hasattr(self, "flags"):
            for f in self.flags:
                _resolved.append(utils.resolve_string(data=self.environment.envs, string=f))
            if len(_resolved) > 0:
                return " ".join(_resolved)
            return " ".join(self.flags)
        return ""

    def __create_launch_command(self, product):
        _directory = self.directory.replace("*", self.version)
        _flags = self.__check_flags()

        if _check_if_resolved(string=_flags) is False:
            _flags = ""

        _command = "{cmd} '{dir}' {flags}".format(cmd=self.environment.envs["_launch"], dir=os.path.join(_directory, self.products[product]), flags=_flags)
        return _command


def _check_if_resolved(string):
    if "{" not in string and "}" not in string:
        return True
    return False


def _parse_arguments(arguments):
    if arguments:
        arguments = utils.remove_all_characters(chars=["[", "]", ",", "'"], string=arguments)
        arguments = arguments.split(" ")
        arguments.pop(0)
        if arguments:
            _args = {"project": arguments[0], "context": arguments[1], "task": arguments[2], "department": arguments[3], "product": arguments[4]}
            env = Environment(**_args)


if __name__ == '__main__':
    _parse_arguments(arguments=str(sys.argv))
