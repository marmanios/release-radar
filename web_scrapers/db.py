# db.py

from sqlalchemy import create_engine
from sqlalchemy import insert
from sqlalchemy.engine import Engine
from utils.helpful_types import RefinedOutput
from dotenv import load_dotenv
from os import getenv
from sqlalchemy import Table, MetaData
from logger import setup_logger
import re, string; 
# import pandas as pd

load_dotenv()

def get_engine() -> Engine:
    """
    Creates and returns a SQLAlchemy engine.
    """
    db_url = getenv("DB_URL")
    if not db_url:
        raise ValueError("Database URL not found in environment variables.")
    
    return create_engine(db_url)

def check_if_patch_exists(source: str, version: str) -> bool:
    """
    Checks if a patch with the given source and version already exists in the database.

    Args:
        source (str): The source of the patch.
        version (str): The version of the patch.
        db_engine (Engine): SQLAlchemy engine to connect to the database.

    Returns:
        bool: True if the patch exists, False otherwise.
    """
    db_engine = get_engine()

    meta = MetaData()
    patch_notes_table = Table('patch_notes', meta, autoload_with=db_engine)

    with db_engine.connect() as connection:
        query = patch_notes_table.select().where(
            (patch_notes_table.c.source == source) & 
            (patch_notes_table.c.version == version)
        )
        result = connection.execute(query).fetchone()
    
    return result is not None

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

    db_engine = get_engine()

    # get the table
    meta = MetaData()
    patch_notes_table = Table('patch_notes', meta, autoload_with=db_engine)


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
            "version": re.sub(r'[^a-zA-Z0-9._\-]+', ' ', item['version']).strip(),
            "ai_summary": item['changes_markdown'],
        } for item in data
    ])

    # Execute the insert statement
    with db_engine.connect() as connection:
        result = connection.execute(stmt)
        connection.commit()
        print("Data loaded successfully into the database.")
        print(f"Inserted {result.rowcount} rows.")