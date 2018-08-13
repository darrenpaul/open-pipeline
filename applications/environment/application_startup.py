import os
from utils import utils
from pprint import pprint


def setup_application(environment):
    if "appname" in environment.envs:
        _app_function = "_setup_{app}".format(app=environment.envs["appname"])
        globals()[_app_function](environment)


def _setup_houdini(environment):
    import copy
    print "Houdini"
    _version = environment.envs["appversion"].split(".")
    _version.pop(len(_version) - 1)
    _version = ".".join(_version)
    _userhou = os.path.expanduser("~")

    if environment.envs["os"] == "windows":
        _userhou = os.path.join(_userhou, "Documents", "houdini{version}".format(version=_version))
    elif environment.envs["os"] == "linux":
        _userhou = os.path.join(_userhou, "houdini{version}".format(version=_version))

    if os.path.exists(_userhou) is False:
        os.makedirs(_userhou)
    if os.path.exists(os.path.join(_userhou, "houdini.env")) is False:
        f = open(os.path.join(_userhou, "houdini.env"), "w+")
        f.close()

    _data = utils.read_yaml(path=environment.configs["houdini"])

    _universal = utils.parse_application_environment_config(envs=environment.envs, config=_data, key="universal")

    _platform = utils.parse_application_environment_config(envs=environment.envs, config=_data, key=environment.platform)

    utils.merge_dictionaries(original=_universal, new=_platform)

    _config = {}
    for k, v in _universal.iteritems():
        _config.update({k: ";".join(v)})

    with open(os.path.join(_userhou, "houdini.env"), "w") as f:
        f.write("#   Houdini Environment Settings")
        f.write("\n")
        for k, v in _config.iteritems():
            f.write("{k}={v}\n".format(k=k, v=v))


def _setup_maya(environment):
    _data = utils.read_yaml(path=environment.configs["maya"])
    _universal = utils.parse_application_environment_config(envs=environment.envs, config=_data, key="universal")
    _platform = utils.parse_application_environment_config(envs=environment.envs, config=_data, key=environment.platform)
    utils.merge_dictionaries(original=_universal, new=_platform)

    _config = {}
    for k, v in _universal.iteritems():
        _config.update({k: ";".join(v)})

    os.environ.update(environment.envs)
    os.environ.update(_config)


def _setup_photoshop(environment):
    pass