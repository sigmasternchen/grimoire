from grimoiressg.modules.markdown import compile_markdown
from grimoiressg.modules.tags import extract_tags
from grimoiressg.modules.templating import render_templates

available_modules = {
    "tags": extract_tags,
    "markdown": compile_markdown,
    "templating": render_templates
}


def load_external_module(module):
    __import__(module)
