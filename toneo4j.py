from neo4j import GraphDatabase
import pandas as pd

# konfigurasi koneksi neo4j
uri = "bolt://localhost:7687"
user = "neo4j"
password = "Pumkin!!22" 

driver = GraphDatabase.driver(uri, auth=(user, password))


def import_users(tx, df):
    query = """
    MERGE (u:User {id_user: $id_user})
    SET u.authors = $authors,
        u.region = $region,
        u.age = $age
    """
    for _, row in df.iterrows():
        tx.run(query,
               id_user=int(row['id_user']),
               authors=row['authors'],
               region=row['region'],
               age=int(row['age']))


def import_articles(tx, df):
    query = """
    MERGE (a:Article {id_artikel: $id_artikel})
    SET a.link = $link,
        a.headline = $headline,
        a.category = $category,
        a.date = date($date)
    """
    for _, row in df.iterrows():
        tx.run(query,
               id_artikel=int(row['id_artikel']),
               link=row['link'],
               headline=row['headline'],
               category=row['category'],
               date=row['date'])


def import_relationships(tx, df):
    query = """
    MATCH (u:User {id_user: $id_user})
    MATCH (a:Article {id_artikel: $id_artikel})
    MERGE (u)-[:WROTE]->(a)
    """
    for _, row in df.iterrows():
        tx.run(query,
               id_user=int(row['id_user']),
               id_artikel=int(row['id_artikel']))


def main():
    # load csv pake pandas
    users_df = pd.read_csv('graphuserFinal.csv')
    articles_df = pd.read_csv('grapharcFinal.csv')
    relationships_df = pd.read_csv('graphrelaFinal.csv')

    with driver.session() as session:
        session.write_transaction(import_users, users_df)
        session.write_transaction(import_articles, articles_df)
        session.write_transaction(import_relationships, relationships_df)

    print("import selesai")


if __name__ == "__main__":
    main()