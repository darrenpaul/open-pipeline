def write_yaml(path, data):
    try:
        import yaml
        with open(path, "w+") as yfile:
            yaml.dump(data, yfile, default_flow_style=False)
    except:
        raise ImportError("Failed to import yaml module please install pyyaml through pip E.G. 'pip install pyyaml'")


def read_yaml(path):
    """
    :param path: Path to the config template
    :return: dictionary of the data in the template
    """
    try:
        import yaml
        if os.path.exists(path):
            with open(path) as stream:
                return yaml.load(stream)
    except:
        raise ImportError("Failed to import yaml module please install pyyaml through pip E.G. 'pip install pyyaml'")