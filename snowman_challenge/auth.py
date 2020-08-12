"""Auth module package."""
from typing import Dict

from passlib.hash import pbkdf2_sha256

from snowman_challenge.exceptions import AuthError
from snowman_challenge.models import User as UserModel


def authenticate(username: str, password: str) -> UserModel:
    """Autentication Rule.

    :param username: string containing username
    :param password: string containing password
    :raises AuthError: Invalid username or password
    :return: A user entity
    """
    user = UserModel.query.filter_by(username=username).first()
    if user and pbkdf2_sha256.verify(password, user.password.hash):
        return user

    raise AuthError('Invalid username or password!')


def identify(payload: Dict) -> UserModel:
    """Indentify.

    :param payload: a dictionary payload
    :return: A user entity
    """
    user_id = payload['identity']
    return UserModel.query.get(user_id)
