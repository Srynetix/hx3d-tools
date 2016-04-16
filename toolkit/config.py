from utils.frozen_dict import FrozenDict
import yaml
import os

loaded = False
config = None

if not loaded:
    directory = os.path.dirname(os.path.realpath(__file__))
    with open("{}/config.yml".format(directory), "r") as config_content:
        yaml_content = yaml.load(config_content.read())
        config = FrozenDict(yaml_content)
