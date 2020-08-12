"""Test logic.py.
"""
from typing import List

import pytest
from mixer.backend.sqlalchemy import Mixer
from sqlalchemy.exc import IntegrityError

from snowman_challenge import logic
from snowman_challenge.models import Favorite


def test_get_spot_list_should_retrieve_results(mixer_with_spots: Mixer) -> None:
    """Test if get_spot_list retrieve results.

    :param mixer_with_spots: fixture
    """
    expected = [
        {
            'name': 'Some Place 1',
            'latitude': None,
            'longitude': None,
            'user_id': 1,
            'category': 'some category 1',
            'pictures': [],
        },
        {
            'name': 'Some Place 2',
            'latitude': None,
            'longitude': None,
            'user_id': 2,
            'category': 'some category 2',
            'pictures': [],
        },
    ]
    assert expected == logic.get_spot_list()
    assert isinstance(mixer_with_spots, Mixer)


def test_get_spot_list_should_not_retrieve_results(mixer: Mixer) -> None:  # noqa: WPS118
    """Test if get_spot_list not retrieve results.

    :param mixer: fixture
    """
    expected: List = []
    assert expected == logic.get_spot_list()
    assert isinstance(mixer, Mixer)


def test_search_spot_by_name_should_retrieve_results(mixer_with_spots: Mixer) -> None:  # noqa
    """Test if search_spot_by_name retrieve results.

    :param mixer_with_spots: fixture
    """
    expected = [
        {
            'name': 'Some Place 1',
            'latitude': None,
            'longitude': None,
            'user_id': 1,
            'category': 'some category 1',
            'pictures': [],
        },
    ]
    assert expected == logic.search_spot_by_name('some Place 1')
    assert isinstance(mixer_with_spots, Mixer)


def test_search_spot_by_name_should_not_retrieve_results(mixer: Mixer) -> None:  # noqa
    """Test if search_spot_by_name not retrieve results.

    :param mixer: fixture
    """
    expected: List = []
    assert expected == logic.search_spot_by_name('spotland')
    assert isinstance(mixer, Mixer)


def test_register_spot_should_save_successfully(mixer: Mixer) -> None:
    """Test if register spot saves successfully.

    :param mixer: fixture
    """
    user = mixer.blend('snowman_challenge.models.User')
    user.save()
    category = mixer.blend('snowman_challenge.models.Category', name='category')
    category.save()

    payload = {
        'user_id': 1,
        'category_id': 1,
        'name': 'spotname',
    }
    assert logic.register_spot(spot_data=payload) == 1


def test_register_spot_should_raise_integrity_error(mixer: Mixer) -> None:  # noqa
    """Test if register spot raises integrity violation error.

    :param mixer: fixture
    """
    user = mixer.blend('snowman_challenge.models.User')
    user.save()
    category = mixer.blend('snowman_challenge.models.Category', name='category')
    category.save()

    payload = {
        'user_id': 1,
        'category_id': 1,
        'name': 'spotname',
    }
    logic.register_spot(spot_data=payload)

    with pytest.raises(IntegrityError):
        logic.register_spot(spot_data=payload)


def test_add_picture_should_save_successfully(mixer_with_spots: Mixer) -> None:
    """Test if add picture saves successfully.

    :param mixer_with_spots: fixture
    """
    logic.add_picture(spot_id=1, filename='file.png')
    assert isinstance(mixer_with_spots, Mixer)



def test_add_picture_should_raise_integrity_error(mixer_with_spots: Mixer) -> None:  # noqa
    """Test if add picture raises integrity error violation.

    :param mixer_with_spots: fixture
    """
    logic.add_picture(spot_id=1, filename='file.png')
    with pytest.raises(IntegrityError):
        logic.add_picture(spot_id=1, filename='file.png')
    assert isinstance(mixer_with_spots, Mixer)


def test_add_category_should_save_successfully(mixer: Mixer) -> None:
    """Test if add category saves successfully.

    :param mixer: fixture
    """
    assert logic.add_category(category_name='category') == 1
    assert isinstance(mixer, Mixer)


def test_add_category_should_raise_integrity_error(mixer: Mixer) -> None:  # noqa
    """Test if add category raises integrity error violation.

    :param mixer: fixture
    """
    logic.add_category(category_name='category')
    with pytest.raises(IntegrityError):
        logic.add_category(category_name='category')
    assert isinstance(mixer, Mixer)


def test_add_to_favorites_should_successfull(mixer_with_spots: Mixer) -> None:
    """Test if add to favorites saves successfully.

    :param mixer_with_spots: fixture
    """
    assert logic.add_to_favorites(user_id=1, spot_id=1) == 1
    favorite = Favorite.query.get(1)
    favorite.deleted = True
    assert logic.add_to_favorites(user_id=1, spot_id=1) == 1
    favorite.deleted = False
    assert isinstance(mixer_with_spots, Mixer)


def test_add_to_favorites_should_raise_unique_error(mixer_with_spots: Mixer) -> None:  # noqa
    """Test if add to favorites raises unique error violation.

    :param mixer_with_spots: fixture
    """
    logic.add_to_favorites(user_id=1, spot_id=1)
    with pytest.raises(IntegrityError):
        logic.add_to_favorites(user_id=1, spot_id=1)
    assert isinstance(mixer_with_spots, Mixer)
