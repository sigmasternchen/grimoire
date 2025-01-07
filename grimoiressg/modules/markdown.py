import markdown


def compile_markdown(data, context):
    for entry in data:
        if "markdown" in entry:
            print(f"Compiling markdown for {entry['relative_filename']}...")
            entry["markdown_compiled"] = markdown.markdown(entry["markdown"])
