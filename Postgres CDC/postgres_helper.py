import psycopg2
import os

def connect_postgres():
    # Postgres Constants
    PG_HOST = os.environ["PG_HOST"]
    PG_PORT = os.environ["PG_PORT"]
    PG_USER = os.environ["PG_USER"]
    PG_PASSWORD = os.environ["PG_PASSWORD"]
    PG_DATABASE = os.environ["PG_DATABASE"]

    conn = psycopg2.connect(
        database = PG_DATABASE, user = PG_USER, password = PG_PASSWORD, host = PG_HOST, port = PG_PORT
    )
    return conn


def run_query(conn, query: str):
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()

def init_starter_table(table_name: str):
    conn = connect_postgres()
    query = f'''
    CREATE TABLE {table_name} (
            product_id TEXT,
            title TEXT,
            category TEXT,
            sub_category TEXT,
            image_url TEXT,
            brand TEXT,
            description TEXT,
            color TEXT[],
            material TEXT[],
            price NUMERIC,
            rating NUMERIC
        );
    '''
    try:
        run_query(conn, query)
        conn.close()

    except psycopg2.errors.DuplicateObject:
        print(f"The table {table_name} already exists.")
        conn.close()

    else:
        conn.close()

def create_logical_slot(slot_name: str):
    conn = connect_postgres()
    query = f'''
    SELECT pg_create_logical_replication_slot('{slot_name}', 'wal2json');
    '''
    try:
        run_query(conn, query)
        conn.close()

    except psycopg2.errors.DuplicateObject:
        print(f"Replication slot {slot_name} already exists.")
        conn.close()

    else:
        conn.close()


def create_publication_on_table(publication_name: str, table_name: str):
    conn = connect_postgres()
    query = f'''
    CREATE PUBLICATION {publication_name} FOR TABLE {table_name};
    '''
    try:
        run_query(conn, query)
        conn.close()

    except psycopg2.errors.DuplicateObject:
        print(f"Publication {publication_name} already exists.")
        conn.close()
        
    except psycopg2.errors.UndefinedTable:
        print(f"{table_name} not found.")
        raise  # Appropriate use of raise to propagate the exception
    finally:
        conn.close()  # Ensure connection is closed in finally block

def get_changes(conn, slot_name: str):
    query = f'''
    SELECT data FROM pg_logical_slot_get_changes('{slot_name}', NULL, NULL);
    '''
    cur = conn.cursor()
    cur.execute(query)
    records = cur.fetchall()
    cur.close()
    return records
