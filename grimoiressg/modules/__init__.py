from grimoiressg.modules.markdown import compile_markdown
from grimoiressg.modules.sitemaps import generate_sitemaps
from grimoiressg.modules.tags import extract_tags
from grimoiressg.modules.templating import render_templates

available_modules = {
    "tags": extract_tags,
    "markdown": compile_markdown,
    "templating": render_templates,
    "sitemaps": generate_sitemaps,
}


def load_external_module(module):
    __import__(module)
