import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_db():
    """
    Initialize database and create tables
    Supports both MySQL (local) and PostgreSQL (Render)
    """
    db_type = os.getenv('DB_TYPE', 'mysql')
    
    try:
        if db_type == 'postgresql':
            # PostgreSQL initialization for Render
            import psycopg2
            from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
            
            # Connect to PostgreSQL
            connection = psycopg2.connect(
                host=os.getenv('DATABASE_HOST', 'localhost'),
                user=os.getenv('DATABASE_USER', 'postgres'),
                password=os.getenv('DATABASE_PASSWORD', ''),
                database=os.getenv('DATABASE_NAME', 'video_translator')
            )
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = connection.cursor()
            
            # Create Table (PostgreSQL syntax)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS translations (
                    id SERIAL PRIMARY KEY,
                    video_url VARCHAR(255) NOT NULL,
                    source_language VARCHAR(10),
                    target_language VARCHAR(10) NOT NULL,
                    original_text TEXT,
                    translated_text TEXT,
                    audio_path VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            print("✅ PostgreSQL database 'video_translator' and table 'translations' initialized successfully!")
            
        else:
            # MySQL initialization for local development
            import mysql.connector
            
            # Connect to MySQL server (without database)
            db = mysql.connector.connect(
                host=os.getenv('DATABASE_HOST', 'localhost'),
                user=os.getenv('DATABASE_USER', 'root'),
                password=os.getenv('DATABASE_PASSWORD', '')
            )
            cursor = db.cursor()
            
            # Create Database
            database_name = os.getenv('DATABASE_NAME', 'video_translator')
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            cursor.execute(f"USE {database_name}")
            
            # Create Table (MySQL syntax)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS translations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    video_url VARCHAR(255) NOT NULL,
                    source_language VARCHAR(10),
                    target_language VARCHAR(10) NOT NULL,
                    original_text LONGTEXT,
                    translated_text LONGTEXT,
                    audio_path VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            print(f"✅ MySQL database '{database_name}' and table 'translations' initialized successfully!")
        
        cursor.close()
        if db_type == 'postgresql':
            connection.close()
        else:
            db.close()
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        print(f"TIP: Make sure your {db_type.upper()} server is running and credentials in .env are correct.")
        print(f"Current settings: DB_TYPE={db_type}, HOST={os.getenv('DATABASE_HOST', 'localhost')}")

if __name__ == "__main__":
    init_db()
