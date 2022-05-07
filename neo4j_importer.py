import click
from csv import DictReader
from neo4j import GraphDatabase
from dotenv import dotenv_values, load_dotenv

load_dotenv()
config = dotenv_values(".env")
uri = config.get('NEO4J_URI')
username = config.get('NEO4J_USERNAME')
password = config.get('NEO4J_PASSWORD')
database = config.get('NEO4J_DATABASE')
data_dir = config.get('OUTPUT_DIR')


def _get_data():
    with open(f"{data_dir}/keywords2.csv", "r") as csvfile:
        reader = DictReader(csvfile)
        return list(reader)


class Neo4jImporter:

    def __init__(self):
        print(uri)
        print(username)
        print(password)
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        self.driver.close()

    def process(self):
        with self.driver.session() as session:
            data = _get_data()
            for row in data:
                session.write_transaction(self._merge_keywords,
                                          label=row[':LABEL'],
                                          keyword=row['keyword:ID'])

    @staticmethod
    def _merge_keywords(tx, label, keyword):
        result = tx.run(f"CREATE (k:{label}) "
                        f"SET k.keyword = '{keyword}' ")


"""
WITH "https://raw.githubusercontent.com/sabinem/ckan-to-neo4j/main/datasets_to_keywords.csv" AS uri
LOAD CSV WITH HEADERS FROM uri AS row
MERGE (d:Dataset {dataset_identifier:row.dataset_identifier})-[:HAS_KEYWORD]->(k:Keyword {keyword:row.keyword})
"""

@click.command()
def neo4j_importer():
    importer = Neo4jImporter()
    importer.process()
    importer.close()


if __name__ == "__main__":
    neo4j_importer()
