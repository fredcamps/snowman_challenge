"""conftest.py.
"""
from typing import Generator

import pytest
from mixer.backend.sqlalchemy import Mixer

from snowman_challenge.app import create_app
from snowman_challenge.database import db_engine, drop_db, init_db_session


@pytest.fixture()
def mixer() -> Generator:
    """Test db session.

    :yield: Generator
    """
    session = init_db_session()
    yield Mixer(session=session, commit=True)
    drop_db(db_engine)


@pytest.fixture()
def client() -> Generator:
    """Flask app fixture.

    :yield: Generator
    """
    app = create_app('config')
    app.config['TESTING'] = True

    with app.test_client() as cli:
        yield cli
