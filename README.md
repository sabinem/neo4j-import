# CSV Exporter for a ckan instance

The goal of this tool is to export a ckan instance as csv files that can be imported into neo4j.

The following classes are exported with the goal to turn them into neo4j nodes:

- catalogs.csv (derived from ckan harvesters)
- showcases.csv (derived from ckan showcases)
- datasets.csv (derived from ckan datasets)
- distributions (derived from ckan resources)
- groups (derived from ckan groups)
- organizations (derived from ckan organizations)

additional facets will be turned into nodes:

- keywords
- formats
- publishers
- contact points

Relationsships are also written into csv files
