from _distutils_hack import enabled
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime

from app.core.table_class import DateCreateTable


# see https://fastapi.tiangolo.com/tutorial/sql-databases/
class SimpleKeyTable(DateCreateTable):
    __tablename__ = 'simple_key'
    name = Column(String(64), index=True)
    key = Column(String(64), index=True, unique=True)
    enabled = Column(Boolean, default=True)
