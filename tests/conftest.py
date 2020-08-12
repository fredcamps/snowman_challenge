"""conftest.py.
"""
from typing import Generator

import pytest
from mixer.backend.sqlalchemy import Mixer

from snowman_challenge.app import create_app
from snowman_challenge.database import db_engine, drop_db, init_db_session


@pytest.fixture()
def mixer() -> Generator:
    """Mixer fixture.

    :yield: Generator
    """
    session = init_db_session()
    yield Mixer(session=session, commit=True)
    drop_db(db_engine)


@pytest.fixture()
def mixer_with_spots() -> Generator:
    """Mixer with spots fixture.

    :yield: Generator
    """
    session = init_db_session()
    mix = Mixer(session=session, commit=True)
    spot1 = mix.blend(
        'snowman_challenge.models.Spot',
        name='Some Place 1',
        category__name='some category 1',
        user__username='email@example1.com',
    )
    spot1.save()
    spot2 = mix.blend(
        'snowman_challenge.models.Spot',
        name='Some Place 2',
        category__name='some category 2',
        user__username='email@example2.com',
    )
    spot2.save()
    yield mix
    drop_db(db_engine)


@pytest.fixture()
def client() -> Generator:
    """Flask app fixture.

    :yield: Generator
    """
    app = create_app('snowman_challenge.config')
    app.config['TESTING'] = True

    with app.test_client() as cli:
        yield cli
