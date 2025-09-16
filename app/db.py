import databases
import ormar
import sqlalchemy
import time

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(settings.db_url)


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    email: str = ormar.String(max_length=128, unique=True, nullable=False)
    active: bool = ormar.Boolean(default=True, nullable=False)

def init_db():
    # Create all tables. Only used for test/CI.
    engine = sqlalchemy.create_engine(settings.db_url)
    if not try_connect(engine, retries=30, delay=1):
        raise RuntimeError("DB not reachable during startup")
    metadata.create_all(engine)

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

# engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
