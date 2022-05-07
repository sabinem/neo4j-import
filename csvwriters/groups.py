from csv import DictWriter

fieldnames_group = [
    'group_name',
    "title_de",
    "title_fr",
    "title_en",
    "title_it",
]


def group_writer(ogdremote, output_dir):
    groups = ogdremote.action.group_list()
    groups_complete = ogdremote.action.group_list(all_fields=True)
    with open(f"{output_dir}/groups.csv", "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames_group)
        writer.writeheader()
        for group in groups_complete:
            writer.writerow({
                'group_name': group.get('name'),
                'title_de': group.get('title').get('de'),
                'title_fr': group.get('title').get('fr'),
                'title_en': group.get('title').get('en'),
                'title_it': group.get('title').get('it'),
            })
    return groups
