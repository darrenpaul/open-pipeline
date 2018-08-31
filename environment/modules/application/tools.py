import os
import glob
from modules.manipulation import op_string


def set_executable(platform, application_name):
    if platform == "windows":
        application_name = os.path.splitext(application_name)[0]
        application_name = "{app}.exe".format(app=application_name)
    return application_name.replace(os.sep, "/")


def get_all_application_versions(application_path):
    _versions = []
    for ver in get_app_version_from_path(path=application_path):
        _applicationPath = check_if_application_installed(version=ver, application_path=application_path)
        if _applicationPath is not None:
            _versions.append(ver)
    _versions.sort(reverse=True)
    return _versions


def check_if_application_installed(version, application_path):
    _path = application_path.replace("*", version)
    if os.path.exists(_path):
        return _path.replace(os.sep, "/")
    return None

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


def get_app_version_from_path(path):
    _versions = []
    for _p in glob.glob(pathname=path):
        _index = path.find('*')
        if _index > 0:
            _versions.append(_p[_index:].replace(os.sep, "/").split("/")[0].strip())

        if len(_versions) == 0:
            _versions.append("")

    return _versions


def check_if_resolved(string):
    if "{" not in string and "}" not in string:
        return True
    return False


def parse_application_environment_config(envs, config, key):
    import platform
    _config = {}
    if "environment" in config:
        if key in config["environment"]:
            for k, v in config["environment"][key].iteritems():
                _variables = []
                for i in v:
                    _variables.append(op_string.resolve_string(data=envs, string=i))
                _config.update({k: _variables})
    return _config


def create_application_config(path, app, data):
    import json
    # todo create json script to manage reading and writing
    _dataPath = os.path.join(path, app + ".json")
    data.update({"name": app})

    with open(_dataPath, 'w') as _file:
        json.dump(data, _file)
