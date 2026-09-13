from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = 'postgresql+psycopg2://postgres:' + os.environ['MARKETPULSE_DB_PASSWORD'] + '@localhost:5432/marketpulse'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)