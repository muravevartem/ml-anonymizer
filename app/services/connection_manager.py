from typing import List

from fastapi import HTTPException
from sqlalchemy import create_engine, select, inspect
from sqlalchemy.orm.session import Session

from app.model.dbconnection import DbConnection
from app.schemas.connections import ConnectionResponse, ConnectionCreate, DatabaseResponse, ColumnResponse, \
    TableResponse, SchemaResponse


class ConnectionManager:
    @staticmethod
    def create_connection(db: Session, request: ConnectionCreate) -> ConnectionResponse:
        new_db_connection = DbConnection(username=request.username, password=request.password, host=request.host,
                                         database=request.database, port=request.port, )
        db.add(new_db_connection)
        db.commit()
        db.refresh(new_db_connection)
        return ConnectionResponse(id=new_db_connection.id, username=new_db_connection.username,
                                  database=new_db_connection.database,
                                  port=new_db_connection.port,
                                  host=new_db_connection.host, )

    @staticmethod
    def get_connections(db: Session) -> List[ConnectionResponse]:
        connections = db.query(DbConnection).all()
        return [ConnectionResponse(id=connection.id, username=connection.username, database=connection.database,
                                   host=connection.host, port=connection.port) for
                connection in connections]

    @staticmethod
    def delete_connection(db: Session, connection_id: int):
        db.query(DbConnection).filter(DbConnection.id == connection_id).delete()

    @staticmethod
    def get_database_info(db: Session, connection_id: int) -> DatabaseResponse:
        result = db.execute(select(DbConnection).where(DbConnection.id == connection_id))
        db_connection: DbConnection | None = db.query(DbConnection).filter(DbConnection.id == connection_id).first()
        if db_connection is None:
            raise HTTPException(status_code=404, detail="Connection not found")

        connection_url = (f"postgresql+psycopg2://{db_connection.username}:{db_connection.password}"
                          f"@{db_connection.host}:{db_connection.port}/{db_connection.database}")
        temporary_engine = create_engine(connection_url)
        inspector = inspect(temporary_engine)

        schemas = []
        for schema_name in inspector.get_schema_names():
            tables = []
            for table_name in inspector.get_table_names(schema=schema_name):
                columns = []
                for column in inspector.get_columns(schema=schema_name, table_name=table_name):
                    columns.append(ColumnResponse(name=column["name"], type=str(column["type"]), ))
                tables.append(TableResponse(name=table_name, columns=columns))
            schemas.append(SchemaResponse(name=schema_name, tables=tables))
        return DatabaseResponse(name=db_connection.database, schemas=schemas)


connection_manager = ConnectionManager()
