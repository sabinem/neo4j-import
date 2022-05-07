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
    'publisher',
    'contact_points',
    'language',
    'accrual_periodictity',
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


def dataset_writer(datasets, output_dir):
    with open(f"{output_dir}/datasets.csv", "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames_dataset)
        writer.writeheader()
        for dataset in datasets:
            writer.writerow({
                'dataset_identifier': dataset.get('identifier'),
                'name': dataset.get('name'),
                'title_de': dataset.get('title', {}).get('de'),
                'title_fr': dataset.get('title', {}).get('fr'),
                'title_en': dataset.get('title', {}).get('en'),
                'title_it': dataset.get('title', {}).get('it'),
                'description_de': dataset.get('description', {}).get('de'),
                'description_fr': dataset.get('description', {}).get('fr'),
                'description_en': dataset.get('description', {}).get('en'),
                'description_it': dataset.get('description', {}).get('it'),
                'issued': dataset.get('issued'),
                'modified': dataset.get('modified'),
                'landing_page': dataset.get('url'),
                'spatial': dataset.get('spatial'),
                'temporal': dataset.get('temporal'),
                'relation': dataset.get('relation'),
                'publisher': dataset.get('publisher'),
                'contact_points': json.dumps(dataset.get('contact_points')),
                'language': json.dumps(dataset.get('language')),
                'accrual_periodictity': dataset.get('accrual_periodicity'),
            })


def dataset_to_group_writer(datasets, output_dir):
    with open(f"{output_dir}/datasets_to_groups.csv", "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames_dataset_to_groups)
        writer.writeheader()
        for dataset in datasets:
            for group in dataset.get('groups'):
                writer.writerow({
                    'group_name': group.get('name'),
                    'dataset_identifier': dataset.get('identifier'),
                })


def dataset_to_distribution_writer(datasets, output_dir):
    with open(f"{output_dir}/datasets_to_distributions.csv", "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames_dataset_to_distibutions)
        writer.writeheader()
        for dataset in datasets:
            if dataset.get('resources'):
                for resource in dataset.get('resources'):
                    writer.writerow({
                        'dataset_identifier': dataset.get('identifier'),
                        'distribution_id': resource.get('id'),
                    })


def dataset_to_datasets_writer(datasets, output_dir):
    with open(f"{output_dir}/dataset_to_datasets.csv", "w") as csvfile:
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


def dataset_to_organization_writer(datasets, output_dir):
    with open(f"{output_dir}/datasets_to_organizations.csv", "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames_dataset_to_organization)
        writer.writeheader()
        for dataset in datasets:
            organization = dataset.get('organization')
            writer.writerow({
                'organization_name': organization.get('name'),
                'dataset_identifier': dataset.get('identifier'),
            })


def dataset_to_keyword_writer(datasets, output_dir):
    languages = ['de', 'fr', 'it', 'en']
    keywords = {lang: set() for lang in languages}
    datasets_with_keywords = {lang: list() for lang in languages}
    for dataset in datasets:
        dataset_identifier = dataset.get('identifier')
        dataset_keywords = dataset.get('keywords')
        if keywords:
            for lang in languages:
                dataset_with_keyword = (dataset_identifier, dataset_keywords.get(lang))
                datasets_with_keywords[lang].append(dataset_with_keyword)
                for keyword in dataset_keywords.get(lang):
                    keywords[lang].add(keyword)
    for lang in languages:
        with open(f"{output_dir}/keywords_{lang}.csv", "w") as csvfile:
            writer = DictWriter(csvfile, fieldnames=[f'keyword_{lang}'])
            writer.writeheader()
            for keyword in keywords[lang]:
                writer.writerow({
                    f'keyword_{lang}': keyword,
                })
        with open(f"{output_dir}/datasets_to_keywords_{lang}.csv", "w") as csvfile:
            writer = DictWriter(csvfile, fieldnames=['dataset_identifier', f'keyword_{lang}'])
            writer.writeheader()
            for item in datasets_with_keywords[lang]:
                for keyword in item[1]:
                    writer.writerow({
                        'dataset_identifier': item[0],
                        f'keyword_{lang}': keyword,
                    })
