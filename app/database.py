import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}" # postgresql://<username>:<password>@<ip-address/hostname>/<database-name>
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


''' REFER THIS IF NEEDED TO CONNECT TO POSTGRESQL WITHOUT SQLALCHEMY'''
# while True:    
#     try:
#         conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="admin", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection  successful")
#         break
        
#     except Exception as e:
#         print("Database connection failed")
#         print("Error: ", e)
#         time.sleep(2) # wait for 2 seconds before trying to connect again
 