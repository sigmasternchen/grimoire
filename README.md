# Grimoire SSG

Grimoire is a minimalistic Static Site Generator (SSG) designed to simplify the process of 
creating static websites. With Grimoire, most use cases can be addressed without the need 
for programming knowledge — simply modify YAML files to generate your site.

## Features

- **YAML Configuration**: Define your content and structure using simple YAML files.
- **Template Rendering**: Utilize Jinja2 templates for dynamic content generation.
- **Markdown Support**: Write content in Markdown, which is automatically converted to HTML.
- **Tagging System**: Organize your content with tags for easy referencing in templates.
- **File Inclusion**: Include other YAML files to create a modular content structure.

## Getting Started

### Installation

To get started with Grimoire, clone the repository and install the required dependencies:

```bash
git clone https://github.com/sigmasternchen/grimoire-ssg.git
cd grimoire-ssg
poetry install
```

### Usage

To generate your static site, run the Grimoire command with your input YAML files. You can specify an output directory using the `-o` or `--output` flag.

```bash
poetry run python -m grimoire-ssg -o output_directory input_file.yml
```

### Example YAML File

Here is an example of a YAML file that defines a content structure:

```yaml
# (optional) Included files will also be considered for generation.
# If this attribute is missing or empty, no other files will be included.
include:
  - pages/*.yml
  - blog/*.yml

# (optional) List of tags for this file.
# These can be used in templates later to reference this content.
# If this attribute is missing or empty, this file will not be accessible 
# via any tags.
tags:
  - page

# (optional) The file that should be generated from this .yml file.
# If this attribute is missing, no output file will be generated.
output: index.html

# (optional) Path to the template for this .yml file.
# If this attribute is missing, no output will be generated.
# It's also possible to just use `template` without `output`. In that case
# the rendered template can still be accessed by other templates.
template: ../templates/homepage.html

# (optional) The markdown content for this output file.
# If this attribute is missing, the markdown content can not be 
# referenced by the template.
markdown: |
  # Hello, World!

# All other defined attributes are not interpreted by the program, but 
# can still be referenced by a template.
# The following are some examples:
Date: 2025-01-06
Author: Sigma
```

### Template Example

Grimoire uses Jinja2 templates for rendering. Below is an example of a template that 
extends a layout and includes dynamic content:

```jinja
{% extends template_dir + "/layout.templ.html" %}
{% block title %}Homepage{% endblock %}
{% block content %}
    {{ current.markdown_compiled | safe }}

    <h2>My latest blog articles:</h2>
    <ul>
    {% for entry in tags["blog"] %}
        <li><a href="{{ entry.output }}">{{ entry.title }}</a> ({{ entry.date }})</li>
    {% endfor %}
    </ul>
{% endblock %}
```

### Template Parameters

The following parameters are available in your templates:

- `current`: The current content file being rendered.
- `all`: A list of all content files.
- `tags`: A dictionary of tags with corresponding content files.
- `template_dir`: The absolute path to the parent directory of the current template.

The content file objects in the template contain all fields from the corresponding YAML file. 
Additionally, the following fields are defined:
- `filename` is the absolute filename of the yml file.
- `relative_filename` is the filename of the yml file relative to the working directory.
- `markdown_compiled` is the compiled markdown content in HTML form. In combination with the `safe` filter in Jinja2 the markdown content can be output.
- `rendered` is the rendered template of that file. This can be useful for including other pages in a template.


### Output Structure

The output files will be generated in the specified output directory, with paths defined in the `output` attribute of your YAML files.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Jinja2](https://jinja.palletsprojects.com/) for the templating engine.
- [Markdown](https://python-markdown.github.io/) for content formatting.
- [PyYAML](https://pyyaml.org/) for YAML parsing.

---

For more information, please refer to the documentation or the source code.