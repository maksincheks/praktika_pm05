# database/db.py
import psycopg2

# Настройки подключения
DB_CONFIG = {
    'host': 'localhost',
    'port': 5433,
    'dbname': 'basequery',
    'user': 'postgres',
    'password': '1234554321'
}

def get_connection():
    """Получить подключение к базе данных"""
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            dbname=DB_CONFIG['dbname'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            client_encoding='UTF8'
        )
        return conn
    except Exception as e:
        raise Exception(f"Ошибка подключения к БД: {e}")