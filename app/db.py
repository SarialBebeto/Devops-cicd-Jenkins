# database = databases.Database(settings.db_url)
# metadata = sqlalchemy.MetaData()
# def init_db():
import databases
import ormar
import sqlalchemy
import time

from app.config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()

class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database

class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    email: str = ormar.String(max_length=128, unique=True, nullable=False)
    active: bool = ormar.Boolean(default=True, nullable=False)

# Only run table creation after a successful DB connection

def wait_for_db(max_retries=40, initial_delay=5, backoff_factor=2):
    """Wait for DB to become available with exponential backoff."""
    engine = sqlalchemy.create_engine(settings.db_url)
    delay = initial_delay
    for i in range(max_retries):
        try:
            print(f"Attempt {i+1}: Connecting to DB at {settings.db_url}")
            connection = engine.connect()
            connection.close()
            print(f"DB connection successful after {i+1} attempt(s)")
            return True
        except Exception as e:
            print(f"DB not ready, retrying in {delay}s: {e}")
            time.sleep(delay)
            delay = min(delay * backoff_factor, 60)  
    print(f"DB not reachable after {max_retries} attempts")
    return False

def init_db():
    # Create all tables. Only used for test/CI.
    # engine = sqlalchemy.create_engine(settings.db_url)
    # if not try_connect(engine, retries=30, delay=1):
    #     raise RuntimeError("DB not reachable during startup")
    # metadata.create_all(engine)
