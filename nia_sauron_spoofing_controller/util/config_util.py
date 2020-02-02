import configparser
import os
from pathlib import Path


class ConfigUtil:

    config_file_path = os.path.join(
        Path(__file__).parents[2], "properties.cfg")
    parser = configparser.ConfigParser()

    def __init__(self):
        self.parser.read(self.config_file_path)

    def get(self, section, config):
        return self.parser[section][config]
