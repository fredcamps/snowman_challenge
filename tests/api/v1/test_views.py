"""
Tests for views from API v1.
"""
import json

from flask.testing import FlaskClient


def test_spot_list_should_retrieve_200(client: FlaskClient) -> None:
    """Test if spot list return 200 http status.

    :param client: fixture
    """
    response = client.get('/api/v1/spots/1')
    assert response.status_code == 200


def test_spot_add_should_retrieve_201(client: FlaskClient) -> None:
    """Test if spot add return 201 http status.

    :param client: fixture
    """
    client.post(
        '/api/v1/user',
        data=json.dumps({'username': 'admin', 'password': 'admin'}),
        content_type='application/json',
    )
    response_auth = client.post(
        '/auth',
        data=json.dumps({'username': 'admin', 'password': 'admin'}),
        content_type='application/json',
    )
    token = response_auth.json.get('access_token')
    authorization = 'JWT {0}'.format(token)
    payload = {
        'name': 'Nome',
        'user_id': 1,
        'category_id': 1,
    }
    response = client.post(
        '/api/v1/spots',
        data=json.dumps(payload),
        headers={'Authorization': authorization},
        content_type='application/json',
    )
    assert response.status_code == 201


def test_spot_add_should_retrieve_409(client: FlaskClient) -> None:
    """Test if spot add return 409 http status.

    :param client: fixture
    """
    client.post(
        '/api/v1/user',
        data=json.dumps({'username': 'admin', 'password': 'admin'}),
        content_type='application/json',
    )
    response_auth = client.post(
        '/auth',
        data=json.dumps({'username': 'admin', 'password': 'admin'}),
        content_type='application/json',
    )
    token = response_auth.json.get('access_token')
    authorization = 'JWT {0}'.format(token)
    payload = {
        'name': 'Nome',
        'user_id': 1,
        'category_id': 1,
    }
    client.post(
        '/api/v1/spots',
        data=json.dumps(payload),
        headers={'Authorization': authorization},
        content_type='application/json',
    )
    response = client.post(
        '/api/v1/spots',
        data=json.dumps(payload),
        headers={'Authorization': authorization},
        content_type='application/json',
    )

    assert response.status_code == 409


def test_spot_search_should_retrieve_404(client: FlaskClient) -> None:
    """Test if spot search return 404 http status.

    :param client: fixture
    """

def test_spot_search_should_retrieve_200(client: FlaskClient) -> None:
    """Test if spot search return 200 http status.

    :param client: fixture
    """


def test_category_add_should_retrieve_409(client: FlaskClient) -> None:
    """Test if category add return 409 http status.

    :param client: fixture
    """


def test_category_add_should_retrieve_201(client: FlaskClient) -> None:
    """Test if category add return 201 http status.

    :param client: fixture
    """


def test_picture_add_should_retrieve_409(client: FlaskClient) -> None:
    """Test if picture add return 409 http status.

    :param client: fixture
    """


def test_picture_delete_should_retrieve_200(client: FlaskClient) -> None:
    """Test if picture delete return 200 http status.

    :param client: fixture
    """


def test_favorite_list_should_retrieve_200(client: FlaskClient) -> None:
    """Test if favorite list return 200 http status.

    :param client: fixture
    """


def test_favorite_add_should_retrieve_409(client: FlaskClient) -> None:
    """Test if favorite add return 409 http status.

    :param client: fixture
    """


def test_favorite_add_should_retrieve_201(client: FlaskClient) -> None:
    """Test if favorite add return 201 http status.

    :param client: fixture
    """


def test_favorite_delete_should_retrieve_200(client: FlaskClient) -> None:
    """Test if favorite delete return 200 http status.

    :param client: fixture
    """
