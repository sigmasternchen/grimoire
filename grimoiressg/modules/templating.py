import os

from grimoiressg.utils import to_relative

from jinja2 import Environment, FileSystemLoader

jinja_env = Environment(
    loader=FileSystemLoader("/")
)


def render_templates(data, context):
    files_written = 0

    for entry in data:
        if "template" in entry:
            template_path = os.path.realpath(os.path.dirname(entry["filename"]) + "/" + entry["template"])
            template_dir = os.path.dirname(template_path)
            print(f"Rendering template for {entry['relative_filename']}...")
            template = jinja_env.get_template(template_path)
            entry["rendered"] = template.render(
                **context,
                current=entry,
                all=data,
                template_dir=template_dir
            )

        if "rendered" in entry and "output" in entry:
            files_written += 1
            filename = os.path.realpath(context["output_dir"] + "/" + entry["output"])
            print(f" writing to {to_relative(filename)}")
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as file:
                file.write(entry["rendered"])

    print(f"{files_written} rendered")
