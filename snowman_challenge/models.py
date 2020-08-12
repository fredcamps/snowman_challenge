"""Models for snowman challenge.  # noqa: WPS226
"""
# pylint: disable=too-few-public-methods
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils.types import EmailType, PasswordType


class BaseClass:
    """Base model class.
    """

    def save(self) -> None:
        """Save records method.
        """
        self.query.session.add(self)
        self.query.session.commit()


Base = declarative_base(cls=BaseClass)


class User(Base):
    """User model.
    """

    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)  # noqa: VNE003, WPS125
    username = sa.Column(EmailType, unique=True)
    password = sa.Column(PasswordType(schemes=['pbkdf2_sha256']))
    spots = sa.orm.relationship('Spot', back_populates='user')
    favorites = sa.orm.relationship('Favorite', back_populates='user')


class Category(Base):
    """Category for spots.
    """

    __tablename__ = 'category'

    id = sa.Column(sa.Integer, primary_key=True)  # noqa: VNE003, WPS125
    name = sa.Column(sa.String, unique=True)
    spots = sa.orm.relationship('Spot', back_populates='category')


class Spot(Base):
    """Tourist spots.
    """

    __tablename__ = 'spot'

    id = sa.Column(sa.Integer, primary_key=True)  # noqa: VNE003, WPS125
    name = sa.Column(sa.String, unique=True, nullable=False)
    latitude = sa.Column(sa.String)
    longitude = sa.Column(sa.String)
    user = sa.orm.relationship('User', back_populates='spots')
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), nullable=False)
    category = sa.orm.relationship('Category', back_populates='spots')
    category_id = sa.Column(sa.Integer, sa.ForeignKey('category.id'), nullable=False)
    pictures = sa.orm.relationship('Picture', back_populates='spot')
    favorites = sa.orm.relationship('Favorite', back_populates='spot')


class Picture(Base):
    """Spot pictures.
    """

    __tablename__ = 'picture'

    id = sa.Column(sa.Integer, primary_key=True)  # noqa: VNE003, WPS125
    filename = sa.Column(sa.String, nullable=False, unique=True)
    spot = sa.orm.relationship('Spot', back_populates='pictures')
    spot_id = sa.Column(sa.Integer, sa.ForeignKey('spot.id'), nullable=False)
    deleted = sa.Column(sa.Boolean, nullable=False, default=False)


class Favorite(Base):
    """User spot bookmarks.
    """

    __tablename__ = 'favorite'
    __table_args__ = (sa.UniqueConstraint('user_id', 'spot_id', name='favorite_user_spot_idx'),)

    id = sa.Column(sa.Integer, primary_key=True)  # noqa: VNE003, WPS125
    user = sa.orm.relationship('User', back_populates='favorites')
    spot = sa.orm.relationship('Spot', back_populates='favorites')
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), nullable=False)
    spot_id = sa.Column(sa.Integer, sa.ForeignKey('spot.id'), nullable=False)
    deleted = sa.Column(sa.Boolean, nullable=False, default=False)
