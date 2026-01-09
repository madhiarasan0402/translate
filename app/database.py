import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    """
    Get database connection with support for both MySQL (local) and PostgreSQL (Render)
    """
    db_type = os.getenv('DB_TYPE', 'mysql')  # Default to mysql for local dev
    
    try:
        if db_type == 'postgresql':
            # PostgreSQL connection for Render
            import psycopg2
            from psycopg2.extras import RealDictCursor
            
            connection = psycopg2.connect(
                host=os.getenv('DATABASE_HOST', 'localhost'),
                user=os.getenv('DATABASE_USER', 'postgres'),
                password=os.getenv('DATABASE_PASSWORD', ''),
                database=os.getenv('DATABASE_NAME', 'video_translator'),
                cursor_factory=RealDictCursor,
                connect_timeout=10
            )
            return connection
        else:
            # MySQL connection for local development
            import mysql.connector
            
            connection = mysql.connector.connect(
                host=os.getenv('DATABASE_HOST', 'localhost'),
                user=os.getenv('DATABASE_USER', 'root'),
                password=os.getenv('DATABASE_PASSWORD', ''),
                database=os.getenv('DATABASE_NAME', 'video_translator'),
                connection_timeout=10
            )
            return connection
            
    except Exception as err:
        print(f"Database connection error: {err}")
        return None
