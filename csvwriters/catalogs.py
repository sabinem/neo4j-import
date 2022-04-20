from csv import DictWriter

fieldnames_catalog = [
    'source_id',
    'name',
    'title',
    'url',
    'source_type',
]


def catalog_writer(ogdremote):
    fq = "dataset_type:harvest"
    result = ogdremote.action.package_search(fq=fq, rows=100)
    if not result.get('count'):
        return []
    harvesters = result.get('results')
    with open('catalogs.csv', "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames_catalog)
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
