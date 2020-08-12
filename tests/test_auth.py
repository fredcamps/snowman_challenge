"""Test Auth."""
from mixer.backend.sqlalchemy import Mixer

from snowman_challenge.auth import authenticate


def test_authenticate_should_works(mixer: Mixer) -> None:
    """Test app.

    :param mixer: fixture replacement lkibrary object
    """
    user = mixer.blend(  # noqa: S106
        'snowman_challenge.models.User',
        username='email@provider.com',
        password='123456',
    )
    user.save()

    autenticated = authenticate(username='email@provider.com', password='123456')  # noqa: S106
    assert autenticated.id == user.id
