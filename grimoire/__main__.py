import argparse
import glob
import os
import sys

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader
from yaml import Loader

jinja_env = Environment(
    loader=FileSystemLoader("/")
)


def compile_markdown(data):
    for entry in data:
        if "markdown" in entry:
            print(f"Compiling markdown for {entry['filename']}...")
            entry["markdown_compiled"] = markdown.markdown(entry["markdown"])


def render(data, tags, output_dir):
    for entry in data:
        if "template" in entry:
            template_path = os.path.realpath(os.path.dirname(entry["filename"]) + "/" + entry["template"])
            template_dir = os.path.dirname(template_path)
            print(f"Rendering template for {entry['filename']}...")
            template = jinja_env.get_template(template_path)
            entry["rendered"] = template.render(current=entry, all=data, tags=tags, template_dir=template_dir)

        if "rendered" in entry and "output" in entry:
            filename = os.path.realpath(output_dir + "/" + entry["output"])
            print(f"  ... writing to {filename}")
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as file:
                file.write(entry["rendered"])


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
    print(f"Reading {filename}...")

    with open(filename, "r") as file:
        data = yaml.load(file, Loader)

    data["filename"] = filename
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
    if len(sys.argv) < 2:
        print("no files to work on")
        exit(1)

    output_dir, filenames = parse_arguments()

    print(f"Output directory: {output_dir}")
    print(f"Initial filenames: {filenames}")
    print()

    data = []
    for filename in filenames:
        data.extend(handle_file_or_glob(filename))

    print(f"Total number of entries: {len(data)}")

    compile_markdown(data)
    tags = extract_tags(data)

    render(data, tags, output_dir)


if __name__ == "__main__":
    main()
