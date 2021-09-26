from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime

from app.core.table_class import DateCreateTable


# see https://fastapi.tiangolo.com/tutorial/sql-databases/
class SimpleKeyTable(DateCreateTable):
    __tablename__ = 'simple_key'
    key = Column(String(48), index=True, unique=True)
