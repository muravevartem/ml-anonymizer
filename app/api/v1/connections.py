from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.connections import ConnectionResponse, ConnectionCreate, DatabaseResponse
from app.services.connection_manager import connection_manager

router = APIRouter(prefix="/connections", tags=["connections"])


@router.post("", response_model=ConnectionResponse, status_code=201)
def create_connection(db_connection: ConnectionCreate, db: Session = Depends(get_db)) -> ConnectionResponse:
    return connection_manager.create_connection(db, db_connection)


@router.get("", response_model=list[ConnectionResponse], status_code=200)
def read_connections(db: Session = Depends(get_db)) -> list[ConnectionResponse]:
    return connection_manager.get_connections(db)


@router.delete("/{connection_id}", status_code=204)
def delete_connection(connection_id: int, db: Session = Depends(get_db)):
    connection_manager.delete_connection(db, connection_id)


@router.get("/{connection_id}/database", response_model=DatabaseResponse)
def get_database(connection_id: int, db: Session = Depends(get_db)) -> DatabaseResponse:
    return connection_manager.get_database_info(db, connection_id)
