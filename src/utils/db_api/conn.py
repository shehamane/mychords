from gino.schema import GinoSchemaVisitor
from .api import db

from data.config import PG_HOST, PG_USER, PG_PASS, PG_DBNAME


async def create_db():
    await db.set_bind(f"postgresql://postgres:postgres@db/kurichords_db")
    db.gino: GinoSchemaVisitor
    await db.gino.create_all()
