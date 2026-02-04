from sqlalchemy import Column, Integer, String

from app.database.database import Base


class DbConnection(Base):
    __tablename__ = "db_connection"

    id = Column(Integer, primary_key=True)
    host = Column(String)
    port = Column(Integer)
    username = Column(String)
    password = Column(String)
    database = Column(String)