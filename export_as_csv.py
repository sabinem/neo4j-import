import ckanapi
import click
import csv
import datetime
import logging

log = logging.getLogger(__name__)

def process(ogdremote):
    datasets = []
    organizations = _organizations_writer(ogdremote)
    _group_writer(ogdremote)
    _catalog_writer(ogdremote)
    _showcase_writer(ogdremote)
    for organization in organizations:
        organization_datasets = _search_packages_for_organization(ogdremote, organization)
        datasets.extend(organization_datasets)
    _dataset_writer(datasets)
    _dataset_to_datasets_writer(datasets)
    _dataset_to_group_writer(datasets)
    _dataset_to_organization_writer(datasets)
    _distribution_writer(datasets)
    _dataset_to_distribution_writer(datasets)


def _search_packages_for_organization(ogdremote, organization):
    rows = 500
    page = 0
    result_count = 0
    fq = f"organization:({organization})"
    datasets = []
    processed_count = 0
    while page == 0 or processed_count < result_count:
        try:
            page = page + 1
            start = (page - 1) * rows
            result = ogdremote.action.package_search(
                fq=fq, rows=rows, start=start)
            if not result_count:
                result_count = result['count']
            datasets_in_result = result.get('results')
            for dataset in datasets_in_result:
                print(dataset.get('name'))
                datasets.append(dataset)
            processed_count += len(datasets_in_result)
        except Exception as e:
            print(f"Error occured while searching for packages with fq: {fq}, error: {e}")
    return datasets


def _dataset_writer(datasets):
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
    with open('datasets.csv', "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_dataset)
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


def _dataset_to_group_writer(datasets):
    fieldnames_dataset_to_groups = [
        "group_name",
        "dataset_identifier",
    ]
    with open('datasets_to_groups.csv', "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_dataset_to_groups)
        writer.writeheader()
        for dataset in datasets:
            for group in dataset.get('groups'):
                writer.writerow({
                    'group_name': group.get('name'),
                    'dataset_identifier': dataset.get('identifier'),
                })


def _dataset_to_organization_writer(datasets):
    fieldnames_dataset_to_organization = [
        "organization_name",
        "dataset_identifier",
    ]
    with open('datasets_to_organizations.csv', "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_dataset_to_organization)
        writer.writeheader()
        for dataset in datasets:
            organization = dataset.get('organization')
            writer.writerow({
                'organization_name': organization.get('name'),
                'dataset_identifier': dataset.get('identifier'),
            })


def _distribution_writer(datasets):
    fieldnames_distribution = [
        "distribution_id",
        "format",
        "media_type",
        "download_url",
        "rights",
    ]
    with open('distributions.csv', "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_distribution)
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


def _dataset_to_distribution_writer(datasets):
    fieldnames_dataset_to_distibutions = [
        "dataset_identifier",
        "distribution_id",
    ]
    with open('datasets_to_distributions.csv', "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_dataset_to_distibutions)
        writer.writeheader()
        for dataset in datasets:
            if dataset.get('resources'):
                for resource in dataset.get('resources'):
                    writer.writerow({
                        'dataset_identifier': dataset.get('identifier'),
                        'distribution_id': resource.get('id'),
                    })


def _dataset_to_datasets_writer(datasets):
    fieldnames_dataset_to_datasets = [
        "dataset_identifier",
        "see_also_identifier",
    ]
    with open('dataset_to_datasets.csv', "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_dataset_to_datasets)
        writer.writeheader()
        for dataset in datasets:
            if dataset.get('see_alsos'):
                see_also_list = [item.get('dataset_identifier') for item in dataset.get('see_alsos')]
                for item in see_also_list:
                    writer.writerow({
                        'dataset_identifier': dataset.get('identifier'),
                        'see_also_identifier': item,
                    })


def _organizations_writer(ogdremote):
    organizations = ogdremote.action.organization_list()
    organizations_complete = ogdremote.action.organization_list(all_fields=True, organizations=organizations)
    fieldnames_organization = [
        'organization_name',
        "title_de",
        "title_fr",
        "title_en",
        "title_it",
        "description_de",
        "description_fr",
        "description_en",
        "description_it",
        "url",
    ]
    with open('organizations.csv', "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_organization)
        writer.writeheader()
        for organization in organizations_complete:
            writer.writerow({
                'organization_name': organization.get('name'),
                'title_de': organization.get('title').get('de'),
                'title_fr': organization.get('title').get('fr'),
                'title_en': organization.get('title').get('en'),
                'title_it': organization.get('title').get('it'),
                'description_de': organization.get('description').get('de'),
                'description_fr': organization.get('description').get('fr'),
                'description_en': organization.get('description').get('en'),
                'description_it': organization.get('description').get('it'),
                'url': organization.get('url'),
            })
    return organizations


def _catalog_writer(ogdremote):
    fq = "dataset_type:harvest"
    result = ogdremote.action.package_search(fq=fq, rows=100)
    if not result.get('count'):
        return []
    harvesters = result.get('results')
    fieldnames_catalog = [
        'source_id',
        'name',
        'title',
        'url',
        'source_type',
    ]
    with open('catalogs.csv', "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_catalog)
        writer.writeheader()
        for harvester in harvesters:
            writer.writerow({
                'source_id': harvester.get('id'),
                'name': harvester.get('name'),
                'title': harvester.get('title'),
                'url': harvester.get('url'),
                'source_type': harvester.get('source_type'),
            })
    return harvesters


def _showcase_writer(ogdremote):
    fq = f"dataset_type:showcase"
    result = ogdremote.action.package_search(fq=fq, rows=100)
    if not result.get('count'):
        return []
    showcases = result.get('results')
    fieldnames_showcase = [
        'showcase_name',
        'title',
        'url',
    ]
    with open('showcases.csv', "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_showcase)
        writer.writeheader()
        for showcase in showcases:
            writer.writerow({
                'showcase_name': showcase.get('name'),
                'title': showcase.get('title'),
                'url': showcase.get('url'),
            })
    return showcases


def _group_writer(ogdremote):
    groups = ogdremote.action.group_list()
    groups_complete = ogdremote.action.group_list(all_fields=True)
    fieldnames_group = [
        'group_name',
        "title_de",
        "title_fr",
        "title_en",
        "title_it",
    ]
    with open('groups.csv', "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_group)
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


def _get_log_file_name(ckanurl):
    filename = 'export'
    filename += '.log'
    return filename


@click.command()
@click.option('-c', '--ckanurl',
              help='Provide remote ckan url')
def export_as_csv(ckanurl):
    if not ckanurl:
        raise click.UsageError("remote site url is missing. Please provide a remote ckan site url -c")
    ogdremote = ckanapi.RemoteCKAN(ckanurl)
    try:
        ogdremote.action.status_show()
    except:
        raise click.UsageError("ckanurl is not valid: {}".format(ckanurl))
    logging.basicConfig(
        filename=_get_log_file_name(ckanurl),
        format="%(message)s",
        level=logging.INFO,
        filemode="w",
    )
    log.info("--------------- config ----------------")
    log.info(f"The ckan url is {ckanurl}")
    log.info(f"Start at {datetime.datetime.now()}")
    log.info("--------------- start -----------------")
    process(ogdremote=ogdremote)


if __name__ == '__main__':
    export_as_csv()
