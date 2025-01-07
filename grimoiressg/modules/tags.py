
def extract_tags(data, context):
    tags = {}

    for entry in data:
        for tag in entry.get("tags", []):
            entry_list = tags.get(tag, [])
            entry_list.append(entry)
            tags[tag] = entry_list

    if tags:
        print("Found tags:")
        for tag in tags.keys():
            print(f" - {tag} ({len(tags[tag])} files)")
    else:
        print("No tags found.")

    context["tags"] = tags