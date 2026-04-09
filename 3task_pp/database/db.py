import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'port': 5433,
    'dbname': 'basequery',
    'user': 'postgres',
    'password': '1234554321'
}

def get_connection():
    conn = psycopg2.connect(
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        dbname=DB_CONFIG['dbname'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        client_encoding='UTF8'
    )
    return conn