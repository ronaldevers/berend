import os
import yaml


BEREND_CONFIG = 'BEREND_CONFIG'  # name of environment variable for config file
IRC = 'irc'  # the config file section for irc settings


def get_config_filename(default_filename):
    """Returns the config filename given on the command line or the default."""
    if BEREND_CONFIG in os.environ:
        return os.environ[BEREND_CONFIG]
    return default_filename


def load_config(default_filename):
    """Reads the config file and returns a ConfigParser config object."""
    with open(get_config_filename(default_filename)) as f:
        return yaml.load(f)
