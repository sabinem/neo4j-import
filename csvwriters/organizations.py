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

fieldnames_organization_to_parent_organization = [
    'organization_name',
    'parent_organization_name'
]

fieldnames_organization_to_political_level = [
    'organization_name',
    'political_level_name'
]

fieldnames_political_levels = [
    'political_level_name',
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


def organization_detail_writer(ogdremote, organizations):
    political_levels = []
    parent_organizations = []
    organization_levels = []
    for organization in organizations:
        organization_details = ogdremote.action.organization_show(id=organization)
        political_level = organization_details.get('political_level')
        if not political_level in political_levels:
            political_levels.append(political_level)
        if political_level:
            organization_levels.append((organization, political_level))
        organization_groups = organization_details.get('groups')
        if organization_groups:
            for group in organization_groups:
                parent_organizations.append((organization, group.get('name')))

    with open('organization_to_parent_organization.csv', "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames_organization_to_parent_organization)
        writer.writeheader()
        for organization_pair in parent_organizations:
            writer.writerow({
                'organization_name': organization_pair[0],
                'parent_organization_name': organization_pair[1],
            })
    with open('political_levels.csv', "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames_political_levels)
        writer.writeheader()
        for political_level in political_levels:
            writer.writerow({
                'political_level_name': political_level,
            })
    with open('organization_to_political_level.csv', "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames_organization_to_political_level)
        writer.writeheader()
        for organization_level_pair in organization_levels:
            writer.writerow({
                'organization_name': organization_level_pair[0],
                'political_level_name': organization_level_pair[1],
            })
