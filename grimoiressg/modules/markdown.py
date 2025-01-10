import markdown

from grimoiressg.utils import logger


def compile_markdown(data, context):
    for entry in data:
        if "markdown" in entry:
            logger.debug("Compiling markdown for %s...", entry['relative_filename'])
            entry["markdown_compiled"] = markdown.markdown(entry["markdown"])
