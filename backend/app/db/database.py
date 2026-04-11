import psycopg2
from psycopg2.extras import RealDictCursor
from app.core.config import settings

def get_db_connection():
    try:
        conn=psycopg2.connect(settings.DATABASE_URL)
        return conn
    except Exception as error:
        print(f"Error connecting to the db... Error: {error}")
        return None