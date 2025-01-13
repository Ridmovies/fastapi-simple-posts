from fastapi import APIRouter
from sqlalchemy import text

from src.database import create_db_and_tables, SessionDep

router = APIRouter()

@router.delete("/restart_db")
async def create_db():
    create_db_and_tables()
    return "Database is created"


@router.get("/check-db-connection")
async def check_db_connection(session: SessionDep):
    """Check if the database connection is successful"""
    session.execute(text("SELECT 1"))
    return {"message": "Connection to the database successful"}