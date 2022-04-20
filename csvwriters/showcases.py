from csv import DictWriter

fieldnames_showcase = [
    'showcase_name',
    'title',
    'url',
    'showcase_type',
    'notes',
]
fieldnames_showcase_to_datasets = [
    'showcase_name',
    'dataset_identifier',
]
fieldnames_tags = [
    'tag',
]
fieldnames_application_types = [
    'showcase_name',
    'dataset_identifier',
]
fieldnames_showcases_to_tags = [
    'showcase_name',
    'dataset_identifier',
]
fieldnames_showcases_to_application_types = [
    'showcase_name',
    'dataset_identifier',
]
fieldnames_showcases_to_tags = [
    'showcase_name',
    'dataset_identifier',
]


def showcase_writer(ogdremote):
    fq = f"dataset_type:showcase"
    result = ogdremote.action.package_search(fq=fq, rows=100)
    if not result.get('count'):
        return []

    showcases = result.get('results')

    for showcase in showcases:
        showcase['datasets'] = []
        datasets = ogdremote.action.ckanext_showcase_package_list(showcase_id=showcase['name'])
        if datasets:
            for dataset in datasets:
               showcase['datasets'].append(dataset.get('identifier'))

    with open('showcases.csv', "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames_showcase)
        writer.writeheader()
        for showcase in showcases:
            writer.writerow({
                'showcase_name': showcase.get('name'),
                'title': showcase.get('title'),
                'url': showcase.get('url'),
            })

    with open('showcases_to_datasets.csv', "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames_showcase_to_datasets)
        writer.writeheader()
        for showcase in showcases:
            for dataset_identifier in showcase['datasets']:
                writer.writerow({
                    'showcase_name': showcase.get('name'),
                    'dataset_identifier': dataset_identifier,
                })

    return showcases
