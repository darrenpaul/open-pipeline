import os
from pprint import pprint
from modules.application import tools as app_tools
from modules.read_write import op_yaml
from modules.data import op_dictionary


def setup_application(environment):
    if "appname" in environment.core_variables:
        print environment.core_variables["appname"]
        _app_function = "_setup_{app}".format(app=environment.core_variables["appname"])
        globals()[_app_function](environment)


def _setup_houdini(environment):
    import copy
    print "Houdini"
    _version = environment.core_variables["appversion"].split(".")
    _version.pop(len(_version) - 1)
    _version = ".".join(_version)
    _userhou = os.path.expanduser("~")

    if environment.core_variables["os"] == "windows":
        _userhou = os.path.join(_userhou, "Documents", "houdini{version}".format(version=_version))
    elif environment.core_variables["os"] == "linux":
        _userhou = os.path.join(_userhou, "houdini{version}".format(version=_version))

    if os.path.exists(_userhou) is False:
        os.makedirs(_userhou)
    if os.path.exists(os.path.join(_userhou, "houdini.env")) is False:
        f = open(os.path.join(_userhou, "houdini.env"), "w+")
        f.close()

    _data = op_yaml.read_yaml(path=environment.configs["houdini"])

    _universal = app_tools.parse_application_environment_config(envs=environment.core_variables, config=_data, key="universal")

    _platform = app_tools.parse_application_environment_config(envs=environment.core_variables, config=_data, key=environment.platform)

    op_dictionary.merge_dictionaries(original=_universal, new=_platform)

    _config = {}
    for k, v in _universal.iteritems():
        _config.update({k: ";".join(v)})

    with open(os.path.join(_userhou, "houdini.env"), "w") as f:
        f.write("#   Houdini Environment Settings")
        f.write("\n")
        for k, v in _config.iteritems():
            f.write("{k}={v}\n".format(k=k, v=v))


def _setup_maya(environment):
    _data = op_yaml.read_yaml(path=environment.configs["maya"])
    _universal = app_tools.parse_application_environment_config(envs=environment.core_variables, config=_data, key="universal")
    _platform = app_tools.parse_application_environment_config(envs=environment.core_variables, config=_data, key=environment.platform)
    op_dictionary.merge_dictionaries(original=_universal, new=_platform)

    _config = {}
    for k, v in _universal.iteritems():
        _config.update({k: ";".join(v)})

    os.environ.update(environment.core_variables)
    os.environ.update(_config)


def _setup_photoshop(environment):
    pass