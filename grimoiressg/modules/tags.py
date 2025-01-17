from grimoiressg.utils import logger


def extract_tags(data, context, config):
    tags = {}

    for entry in data:
        for tag in entry.get("tags", []):
            entry_list = tags.get(tag, [])
            entry_list.append(entry)
            tags[tag] = entry_list

    if tags:
        logger.debug("Found tags:")
        for tag in tags.keys():
            logger.debug(" - %s (%d files)", tag, len(tags[tag]))
    else:
        logger.debug("No tags found.")

    context["tags"] = tags