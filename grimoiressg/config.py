import yaml
from yaml import Loader

from grimoiressg.modules import available_modules


def default_config():
    return {
        "enabled_modules": [
            "tags",
            "markdown",
            "templating"
        ]
    }


def read_config(context):
    config_file = context.get("config_file", None)

    if not config_file:
        print("No config file given; using default config")
        config = default_config()
    else:
        with open(config_file, "r") as file:
            config = yaml.load(file, Loader) or {}

    print("Enabled modules:")
    for module in config.get("enabled_modules", []):
        print(f" - {module}")
        if module not in available_modules:
            print(f"    ERROR: Module does not exist")
            exit(1)
    print()

    return config
