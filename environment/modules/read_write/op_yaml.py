import os


def write_yaml(path, data):
    import yaml
    with open(path, "w+") as yfile:
        yaml.dump(data, yfile, default_flow_style=False)


def read_yaml(path):
    """
    :param path: Path to the config template
    :return: dictionary of the data in the template
    """
    import yaml
    if os.path.exists(path):
        with open(path) as stream:
            return yaml.load(stream)