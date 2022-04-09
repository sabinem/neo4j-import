# CSV Exporter for a ckan instance

The goal of this tool is to export a ckan instance as csv files so that can be 
imported into neo4j via the neo4j import tool

## Nodes

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

## Relationships

All Relationsships are also written into csv files

## Install

```
python3 -m venv p3venv
source p3venv/bin/activate
pip install -r requirements.txt
```

## Use

```
python export_as_csv.py -c https://ckan.opendata.swiss
```
