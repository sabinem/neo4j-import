import logging
from csv import DictWriter

log = logging.getLogger(__name__)

fieldnames_catalog = [
    'source_id',
    'name',
    'title',
    'url',
    'source_type',
]


def catalog_writer(ogdremote, output_dir):
    filename = f"{output_dir}/catalogs.csv"
    fieldnames = fieldnames_catalog
    count = 0
    fq = "dataset_type:harvest"
    result = ogdremote.action.package_search(fq=fq, rows=100)
    if not result.get('count'):
        return []
    harvesters = result.get('results')
    with open(f"{output_dir}/catalogs.csv", "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for harvester in harvesters:
            writer.writerow({
                'source_id': harvester.get('id'),
                'name': harvester.get('name'),
                'title': harvester.get('title'),
                'url': harvester.get('url'),
                'source_type': harvester.get('source_type'),
            })
            count += 1
    log.info(f"{count} items were written to {filename}")
    log.info(f"- fieldnames: {fieldnames}")
    return harvesters
