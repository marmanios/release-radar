# db.py

from sqlalchemy import create_engine
from sqlalchemy import insert
from sqlalchemy.engine import Engine
from utils.helpful_types import RefinedOutput
from dotenv import load_dotenv
from os import getenv
from sqlalchemy import Table, MetaData, Column, Date, UUID, Text
from logger import setup_logger

# import pandas as pd

load_dotenv()

def get_engine(database_url: str) -> Engine:
    """
    Creates and returns a SQLAlchemy engine.
    """
    return create_engine(database_url)

def load_to_sql(
    data: list[RefinedOutput],
) -> None:
    """
    Loads RefinedOutput data objects into the patch_notes table.

    Args:
        data (list[RefinedOutput]): List of RefinedOutput objects to load.
    """
    logger = setup_logger("db", "web_scrapers/logs/db.log" )
    logger.info("##############  Starting to load data into the database  ##############")

    db_url = getenv("DB_URL")
    if not db_url:
        raise ValueError("Database URL not found in environment variables.")
    
    db_engine = get_engine(db_url)

    # get the table
    meta = MetaData()
    patch_notes_table = Table(
        'patch_notes', meta, 
        Column('id', UUID, primary_key = True, nullable=False), 
        Column('source', Text, nullable=False), 
        Column('source_url', Text, nullable=False), 
        Column('released_at', Date), 
        Column('version', Text, nullable=False), 
        Column('ai_summary', Text, nullable=False), 
        Column('created_at', Date, nullable=False, server_default='CURRENT_TIMESTAMP'), 
    )

    logger.info(f"Preparing to load data into the database {len(data)} items.")

    if not data:
        logger.warning("No data to load into the database.")
        return

    # Prepare the insert statement
    stmt = insert(patch_notes_table).values([
        {
            "source": item['source'],
            "source_url": item['link'],
            "released_at": item['release_date'],
            "version": item['version'],
            "ai_summary": item['changes_markdown'],
        } for item in data
    ])

    # Execute the insert statement
    with db_engine.connect() as connection:
        result = connection.execute(stmt)
        connection.commit()
        print("Data loaded successfully into the database.")
        print(f"Inserted {result.rowcount} rows.")