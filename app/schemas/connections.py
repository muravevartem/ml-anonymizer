from typing import List

from pydantic import BaseModel


class ConnectionCreate(BaseModel):
    host: str
    port: int
    username: str
    password: str
    database: str

class ConnectionResponse(BaseModel):
    id: int
    host: str
    port: int
    username: str
    database: str

class ColumnResponse(BaseModel):
    name: str
    type: str


class TableResponse(BaseModel):
    name: str
    columns: List[ColumnResponse]


class SchemaResponse(BaseModel):
    name: str
    tables: List[TableResponse]


class DatabaseResponse(BaseModel):
    name: str
    schemas: List[SchemaResponse]
