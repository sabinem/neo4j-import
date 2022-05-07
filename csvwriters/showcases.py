import logging
from csv import DictWriter

log = logging.getLogger(__name__)

fieldnames_showcase = [
    'showcase_name',
    'title',
    'url',
    'notes',
    'image_url',
    'showcase_notes_formatted',
    'image_display_url',
    'author',
    'author_email'
]
fieldnames_showcase_to_datasets = [
    'showcase_name',
    'dataset_identifier',
]
fieldnames_tags = [
    'tag_name',
]
fieldnames_application_types = [
    'application_type_name',
]
fieldnames_showcases_to_tags = [
    'showcase_name',
    'tag_name',
]
fieldnames_showcases_to_application_types = [
    'showcase_name',
    'application_type_name',
]
fieldnames_showcases_to_groups = [
    'showcase_name',
    'group_name',
]


def showcase_writer(ogdremote, output_dir):
    fq = f"dataset_type:showcase"
    result = ogdremote.action.ogdch_showcase_search(fq=fq, rows=100)
    if not result.get('count'):
        return []

    showcases = result.get('results')
    application_types = []
    all_tags = []
    showcases_to_application_types = []
    showcases_to_tags = []
    showcases_to_groups = []

    for showcase in showcases:
        showcase['datasets'] = []
        datasets = ogdremote.action.ckanext_showcase_package_list(showcase_id=showcase['name'])
        if datasets:
            for dataset in datasets:
               showcase['datasets'].append(dataset.get('identifier'))

        showcase_name = showcase.get('name')
        application_type =  showcase.get('showcase_type')
        if application_type not in application_types:
            application_types.append(application_type)
        if application_type:
            showcases_to_application_types.append((showcase_name, application_type))
        tag_names = [tag.get('name') for tag in showcase.get('tags')]
        if tag_names:
            all_tags.extend([tag for tag in tag_names if not tag in all_tags])
            for tag_name in tag_names:
                showcases_to_tags.append((showcase_name, tag_name))
        group_names = [group.get('name') for group in showcase.get('groups')]
        if group_names:
            for group_name in group_names:
                showcases_to_groups.append((showcase_name, group_name))
    filename = f"{output_dir}/showcases.csv"
    fieldnames = fieldnames_showcase
    count = 0
    with open(filename, "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for showcase in showcases:
            writer.writerow({
                'showcase_name': showcase.get('name'),
                'title': showcase.get('title'),
                'url': showcase.get('url'),
                'notes': showcase.get('notes'),
                'showcase_notes_formatted': showcase.get('showcase_notes_formatted'),
                'image_url': showcase.get('image_url'),
                'image_display_url': showcase.get('image_display_url'),
                'author': showcase.get('author'),
                'author_email': showcase.get('author_email'),
            })
            count += 1
    log.info(f"{count} items were written to {filename}")
    log.info(f"- fieldnames: {fieldnames}")
    filename = f"{output_dir}/showcases_to_datasets.csv"
    fieldnames = fieldnames_showcase_to_datasets
    count = 0
    with open(filename, "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for showcase in showcases:
            for dataset_identifier in showcase['datasets']:
                writer.writerow({
                    'showcase_name': showcase.get('name'),
                    'dataset_identifier': dataset_identifier,
                })
            count += 1
    log.info(f"{count} items were written to {filename}")
    log.info(f"- fieldnames: {fieldnames}")
    filename = f"{output_dir}/tags.csv"
    fieldnames = fieldnames_tags
    count = 0
    with open(filename, "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for tag in all_tags:
            writer.writerow({
                'tag_name': tag,
            })
            count += 1
    log.info(f"{count} items were written to {filename}")
    log.info(f"- fieldnames: {fieldnames}")
    filename = f"{output_dir}/application_types.csv"
    fieldnames = fieldnames_application_types
    count = 0
    with open(filename, "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for name in application_types:
            writer.writerow({
                'application_type_name': name,
            })
            count += 1
    log.info(f"{count} items were written to {filename}")
    log.info(f"- fieldnames: {fieldnames}")
    filename = f"{output_dir}/showcases_to_tags.csv"
    fieldnames = fieldnames_showcases_to_tags
    count = 0
    with open(filename, "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for showcase_tag_pair in showcases_to_tags:
            writer.writerow({
                'showcase_name': showcase_tag_pair[0],
                'tag_name': showcase_tag_pair[1],
            })
            count += 1
    log.info(f"{count} items were written to {filename}")
    log.info(f"- fieldnames: {fieldnames}")
    filename = f"{output_dir}/showcases_to_application_types.csv"
    fieldnames = fieldnames_showcases_to_application_types
    count = 0
    with open(filename, "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for showcase_application_type_pair in showcases_to_application_types:
            writer.writerow({
                'showcase_name': showcase_application_type_pair[0],
                'application_type_name': showcase_application_type_pair[1],
            })
            count += 1
    log.info(f"{count} items were written to {filename}")
    log.info(f"- fieldnames: {fieldnames}")
    filename = f"{output_dir}/showcases_to_groups.csv"
    fieldnames = fieldnames_showcases_to_groups
    count = 0
    with open(filename, "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for showcase_group_pair in showcases_to_groups:
            writer.writerow({
                'showcase_name': showcase_group_pair[0],
                'group_name': showcase_group_pair[1],
            })
            count += 1
    log.info(f"{count} items were written to {filename}")
    log.info(f"- fieldnames: {fieldnames}")

    return showcases
