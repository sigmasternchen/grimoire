import yaml
from yaml import Loader

from grimoiressg.modules import available_modules, load_external_module


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
        print("Loading config file...")
        with open(config_file, "r") as file:
            config = yaml.load(file, Loader) or {}

    for module in config.get("load_modules", []):
        print(f" Loading external module {module}")
        load_external_module(module)
    print()

    print("Enabled modules:")
    for module in config.get("enabled_modules", []):
        print(f" - {module}")
        if module not in available_modules:
            print(f"    ERROR: Module does not exist")
            exit(1)
    print()

    return config
