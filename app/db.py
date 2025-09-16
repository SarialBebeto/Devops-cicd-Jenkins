# database = databases.Database(settings.db_url)
# metadata = sqlalchemy.MetaData()
# def init_db():
import databases
import ormar
import sqlalchemy
import time

from .config import settings

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
engine = sqlalchemy.create_engine(settings.db_url)
for i in range(10):
    try:
        connection = engine.connect()
        connection.close()
        break
    except Exception as e:
        print(f"DB not ready, retrying in 3s: {e}")
        time.sleep(3)
else:
    raise RuntimeError("DB not reachable after 10 attempts")

metadata.create_all(engine)

def init_db():
    # Create all tables. Only used for test/CI.
    engine = sqlalchemy.create_engine(settings.db_url)
    if not try_connect(engine, retries=30, delay=1):
        raise RuntimeError("DB not reachable during startup")
    metadata.create_all(engine)
