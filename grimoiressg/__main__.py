from grimoiressg.arguments import parse_arguments_to_initial_context
from grimoiressg.config import read_config
from grimoiressg.content_files import recursively_read_files
from grimoiressg.modules import available_modules


def apply_modules(data, config, context):
    for module in config.get("enabled_modules", []):
        print(f"Applying module {module}...")
        available_modules[module](data, context)
        print("")


def main():
    context = parse_arguments_to_initial_context()
    config = read_config(context)

    data = recursively_read_files(context)
    apply_modules(data, config, context)

    print("Done.")


if __name__ == "__main__":
    main()
