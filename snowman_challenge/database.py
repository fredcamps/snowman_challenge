"""Database setup.
"""
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from snowman_challenge.config import DATABASE_URL
from snowman_challenge.models import Base


def get_db_engine(database_url: str = DATABASE_URL) -> Engine:
    """Retrieve db engine object by database.

    :param database_url: a string containing database_url
    :return: A database engine object
    """
    return create_engine(database_url, convert_unicode=True)


db_engine = get_db_engine(DATABASE_URL)


def get_db_session(engine: Engine) -> Session:
    """Get db session.

    :param engine: a database Engine object
    :return: a object database session
    """
    return scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
        ),
    )


def init_db_session(engine: Engine = db_engine) -> Session:
    """Initializes database.

    :param engine: A database engine object
    :return: A database session object
    """
    session = get_db_session(engine=engine)
    Base.query = session.query_property()
    Base.metadata.create_all(bind=engine)
    return session


def drop_db(engine: Engine) -> None:
    """Drop database.

    :param engine: a database object engine
    """
    Base.metadata.drop_all(bind=engine)
