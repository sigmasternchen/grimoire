import os

import yaml
from yaml import Loader

from grimoiressg.utils.files import for_each_glob, to_relative


def handle_file(filename):
    print(f" Reading {to_relative(filename)}...")

    with open(filename, "r") as file:
        data = yaml.load(file, Loader)

    data["filename"] = filename
    data["relative_filename"] = to_relative(filename)
    results = [data]

    relative_dir = os.path.dirname(filename)
    for filename in data.get("include", []):
        filename = relative_dir + "/" + filename
        sub_data = for_each_glob(filename, handle_file)
        results.extend(sub_data)

    return results


def recursively_read_files(context):
    data = []

    print("Reading content files...")

    for filename in context["filenames"]:
        data.extend(for_each_glob(filename, handle_file))

    print(f"Read {len(data)} files in total.")
    print()

    return data
