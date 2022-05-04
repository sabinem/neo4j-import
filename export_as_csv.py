import ckanapi
import click
import datetime
import logging
import csvwriters.groups as gw
import csvwriters.organizations as ow
import csvwriters.showcases as sw
import csvwriters.datasets as dw
import csvwriters.catalogs as cw
import csvwriters.distributions as distw

log = logging.getLogger(__name__)

def process(ogdremote):
    datasets = []
    organizations = ow.organizations_writer(ogdremote)
    ow.organization_detail_writer(ogdremote, organizations)
    gw.group_writer(ogdremote)
    cw.catalog_writer(ogdremote)
    sw.showcase_writer(ogdremote)
    for organization in organizations:
        organization_datasets = _search_packages_for_organization(ogdremote, organization)
        datasets.extend(organization_datasets)
    dw.dataset_writer(datasets)
    dw.dataset_to_datasets_writer(datasets)
    dw.dataset_to_group_writer(datasets)
    dw.dataset_to_organization_writer(datasets)
    distw.distribution_writer(datasets)
    dw.dataset_to_distribution_writer(datasets)
    dw.dataset_to_keyword_writer(datasets)


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
        filename='export.log',
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
