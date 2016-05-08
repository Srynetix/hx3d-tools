from hx3dtoolkit.utils.frozen_dict import FrozenDict
from hx3dtoolkit.utils.singleton import Singleton
from hx3dtoolkit.utils.color_print import color_print as cprint

import yaml
import yamlordereddictloader
import os
import shutil

class Config(metaclass=Singleton):
    def __init__(self):

        current_directory = os.getcwd()
        toolkit_directory = os.path.dirname(os.path.realpath(__file__))

        # Check if config file exists in current working directory
        if not os.path.isfile("{}/config.yml".format(current_directory)):
            shutil.copy("{}/config.yml".format(toolkit_directory), "{}/config.yml".format(current_directory))
            cprint("> Creating {}/config.yml configuration file.".format(current_directory))

        with open("{}/config.yml".format(current_directory), "r") as config_content:
            yaml_content = yaml.load(config_content.read(), Loader=yamlordereddictloader.Loader)
            self.config = FrozenDict(yaml_content, freeze_children=True)

        with open("{}/dependencies.yml".format(toolkit_directory), "r") as dep_content:
            yaml_content = yaml.load(dep_content.read(), Loader=yamlordereddictloader.Loader)
            self.config["dependencies"] = FrozenDict(yaml_content, freeze_children=True)

config = Config().config
