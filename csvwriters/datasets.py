from csv import DictWriter

fieldnames_dataset = [
    "dataset_identifier",
    "name",
    "title_de",
    "title_fr",
    "title_en",
    "title_it",
    "description_de",
    "description_fr",
    "description_en",
    "description_it",
    "frequency",
    "access_url",
    'issued',
    'modified',
    'landing_page',
    'spatial',
    'temporal',
    'relation',
]

fieldnames_dataset_to_groups = [
    "group_name",
    "dataset_identifier",
]

fieldnames_distribution = [
    "distribution_id",
    "format",
    "media_type",
    "download_url",
    "rights",
]

fieldnames_dataset_to_distibutions = [
    "dataset_identifier",
    "distribution_id",
]

fieldnames_dataset_to_datasets = [
    "dataset_identifier",
    "see_also_identifier",
]

fieldnames_dataset_to_organization = [
    "organization_name",
    "dataset_identifier",
]

def dataset_writer(datasets):
    with open('datasets.csv', "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames_dataset)
        writer.writeheader()
        for dataset in datasets:
            writer.writerow({
                'dataset_identifier': dataset.get('identifier'),
                'name': dataset.get('name'),
                'title_de': dataset.get('title').get('de'),
                'title_fr': dataset.get('title').get('fr'),
                'title_en': dataset.get('title').get('en'),
                'title_it': dataset.get('title').get('it'),
                'description_de': dataset.get('description').get('de'),
                'description_fr': dataset.get('description').get('fr'),
                'description_en': dataset.get('description').get('en'),
                'description_it': dataset.get('description').get('it'),
                'access_url': dataset.get('url'),
                'issued': dataset.get('issued'),
                'modified': dataset.get('modified'),
                'landing_page': dataset.get('landing_page'),
                'spatial': dataset.get('spatial'),
                'temporal': dataset.get('temporal'),
                'relation': dataset.get('relation'),
            })


def dataset_to_group_writer(datasets):
    with open('datasets_to_groups.csv', "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames_dataset_to_groups)
        writer.writeheader()
        for dataset in datasets:
            for group in dataset.get('groups'):
                writer.writerow({
                    'group_name': group.get('name'),
                    'dataset_identifier': dataset.get('identifier'),
                })


def distribution_writer(datasets):
    with open('distributions.csv', "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames_distribution)
        writer.writeheader()
        for dataset in datasets:
            if dataset.get('resources'):
                for resource in dataset.get('resources'):
                    writer.writerow({
                        'distribution_id': resource.get('id'),
                        'format': resource.get('format'),
                        'media_type': resource.get('media_type'),
                        'download_url': resource.get('download_url'),
                        'rights': resource.get('rights'),
                    })


def dataset_to_distribution_writer(datasets):
    with open('datasets_to_distributions.csv', "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames_dataset_to_distibutions)
        writer.writeheader()
        for dataset in datasets:
            if dataset.get('resources'):
                for resource in dataset.get('resources'):
                    writer.writerow({
                        'dataset_identifier': dataset.get('identifier'),
                        'distribution_id': resource.get('id'),
                    })


def dataset_to_datasets_writer(datasets):
    with open('dataset_to_datasets.csv', "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames_dataset_to_datasets)
        writer.writeheader()
        for dataset in datasets:
            if dataset.get('see_alsos'):
                see_also_list = [item.get('dataset_identifier') for item in dataset.get('see_alsos')]
                for item in see_also_list:
                    writer.writerow({
                        'dataset_identifier': dataset.get('identifier'),
                        'see_also_identifier': item,
                    })


def dataset_to_organization_writer(datasets):
    with open('datasets_to_organizations.csv', "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames_dataset_to_organization)
        writer.writeheader()
        for dataset in datasets:
            organization = dataset.get('organization')
            writer.writerow({
                'organization_name': organization.get('name'),
                'dataset_identifier': dataset.get('identifier'),
            })
