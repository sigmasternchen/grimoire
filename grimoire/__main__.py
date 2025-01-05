import argparse
import glob
import os

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader
from yaml import Loader

jinja_env = Environment(
    loader=FileSystemLoader("/")
)


def to_relative(path):
    trimmed = path.removeprefix(os.getcwd())
    if trimmed != path:
        trimmed = "." + trimmed
    return trimmed


def compile_markdown(data):
    for entry in data:
        if "markdown" in entry:
            print(f"Compiling markdown for {entry['relative_filename']}...")
            entry["markdown_compiled"] = markdown.markdown(entry["markdown"])


def render(data, tags, output_dir):
    files_written = 0

    for entry in data:
        if "template" in entry:
            template_path = os.path.realpath(os.path.dirname(entry["filename"]) + "/" + entry["template"])
            template_dir = os.path.dirname(template_path)
            print(f"Rendering template for {entry['relative_filename']}...")
            template = jinja_env.get_template(template_path)
            entry["rendered"] = template.render(current=entry, all=data, tags=tags, template_dir=template_dir)

        if "rendered" in entry and "output" in entry:
            files_written += 1
            filename = os.path.realpath(output_dir + "/" + entry["output"])
            print(f"  ... writing to {to_relative(filename)}")
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as file:
                file.write(entry["rendered"])

    return files_written


def extract_tags(data):
    tags = {}

    for entry in data:
        for tag in entry.get("tags", []):
            entry_list = tags.get(tag, [])
            entry_list.append(entry)
            tags[tag] = entry_list

    print(f"Found tags: " + repr(list(tags.keys())))

    return tags


def handle_file_or_glob(globname):
    results = []

    for filename in glob.glob(os.path.realpath(globname)):
        results.extend(handle_file(filename))

    return results


def handle_file(filename):
    print(f"Reading {to_relative(filename)}...")

    with open(filename, "r") as file:
        data = yaml.load(file, Loader)

    data["filename"] = filename
    data["relative_filename"] = to_relative(filename)
    results = [data]

    relative_dir = os.path.dirname(filename)
    for filename in data.get("include", []):
        filename = relative_dir + "/" + filename
        sub_data = handle_file_or_glob(filename)
        results.extend(sub_data)

    return results


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", default="./output/")

    args, filenames = parser.parse_known_args()

    return args.output, filenames


def main():
    output_dir, filenames = parse_arguments()

    print(f"Output directory: {output_dir}")
    print(f"Initial filenames: {filenames}")
    print()

    if len(filenames) == 0:
        print("error: at least one filename needed")
        exit(1)

    data = []
    for filename in filenames:
        data.extend(handle_file_or_glob(filename))

    print(f"Total number of entries: {len(data)}")
    print()

    compile_markdown(data)
    tags = extract_tags(data)
    files_written = render(data, tags, output_dir)

    print(f"Total files written: {files_written}")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
