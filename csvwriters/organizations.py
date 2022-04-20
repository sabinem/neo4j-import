from csv import DictWriter

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


def organizations_writer(ogdremote):
    organizations = ogdremote.action.organization_list()
    organizations_complete = ogdremote.action.organization_list(all_fields=True, organizations=organizations)
    with open('organizations.csv', "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames_organization)
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
