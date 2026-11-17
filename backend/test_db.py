
from backend.database import engine
from sqlalchemy import text

try:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT DATABASE()")
        )
        print("Database connected successfully!")
        print("Connected Database:", result.scalar())

except Exception as e:
    print("Database connection failed!")
    print(e)
