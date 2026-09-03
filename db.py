from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://postgres:marketpulse_dev@localhost:5432/marketpulse"

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    result = connection.execute(text("SELECT COUNT(*) FROM products;"))
    print(result.scalar())