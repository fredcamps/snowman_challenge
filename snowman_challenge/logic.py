"""Logic layer.  # noqa: WPS202
"""
from typing import Dict, List


from snowman_challenge.config import LIMIT_ROWS
from snowman_challenge.models import (
    Category as CategoryModel,
    Favorite as FavoriteModel,
    Picture as PictureModel,
    Spot as SpotModel,
    User as UserModel
)


def _format_spot_output_list(spots: List) -> List:
    output_list = []
    for spot in spots:
        output_list.append(
            {
                'name': spot.name,
                'latitude': spot.latitude,
                'longitude': spot.longitude,
                'user_id': spot.user_id,
                'category': spot.category.name,
                'pictures': [{'filename': pic.filename} for pic in spot.pictures if not pic.deleted],
            },
        )

    return output_list


def add_user(username: str, password: str) -> int:
    """Add new user.

    :param username: username
    :param password: password

    :return: id of added user
    """
    user = UserModel()
    user.username = username
    user.password = password
    user.save()

    return user.id


def get_spot_list(page: int = 0) -> List:
    """List all tourists spots.

    :param page: Page Number
    :return: A list with spots
    """
    offset = (LIMIT_ROWS * page) - LIMIT_ROWS
    spots = SpotModel.query.order_by(SpotModel.id).limit(LIMIT_ROWS).offset(offset)
    return _format_spot_output_list(spots)


def search_spot_by_name(spot_name: str) -> List:
    """Search spot by name.

    :param spot_name: String that contains name for search
    :return: A list with spots found
    """
    search = '%{0}%'.format(spot_name)
    spots = SpotModel.query.filter(SpotModel.name.ilike(search))
    return _format_spot_output_list(spots)


def register_spot(spot_data: Dict) -> int:
    """Register new spot.

    :param spot_data: A dict with spot data.
    :return: id of registered spot
    """
    spot = SpotModel()
    spot.name = spot_data.get('name')
    spot.user_id = spot_data.get('user_id')
    spot.category_id = spot_data.get('category_id')
    spot.save()

    return spot.id


def add_picture(spot_id: int, filename: str) -> int:
    """Add new picture to spot.

    :param spot_id: Id of spot
    :param filename: A filename of picture
    :return: id of picture added
    """
    picture = PictureModel()
    picture.spot_id = spot_id
    picture.filename = filename
    picture.save()

    return picture.id


def remove_picture(picture_id: int) -> int:
    """Remove picture from spot.

    :param picture_id: Id of picture that will be deleted.
    :return: id of deleted picture
    """
    picture = PictureModel.query.get(picture_id)
    picture.deleted = True
    picture.save()

    return picture.id


def add_to_favorites(user_id: int, spot_id: int) -> int:
    """Add spot to favorites list.

    :param user_id: id of user favorite list
    :param spot_id: id of spot
    :return: id of favorite added
    """
    favorite = FavoriteModel.query.filter_by(user_id=user_id).filter_by(spot_id=spot_id).first()
    if favorite and favorite.deleted:
        favorite.deleted = False
    else:
        favorite = FavoriteModel()
        favorite.user_id = user_id
        favorite.spot_id = spot_id

    favorite.save()

    return favorite.id


def remove_from_favorites(favorite_id: int) -> int:
    """Remove from favorites.

    :param favorite_id: id of favorite registry
    :return: id of removed favorite
    """
    favorite = FavoriteModel.query.get(favorite_id)
    favorite.deleted = True
    favorite.save()

    return favorite.id


def list_favorites_spots(user_id: int) -> List:
    """List of favorites spots.

    :param user_id: id of user
    :return: list of favorites
    """
    return FavoriteModel.query.filter_by(user_id=user_id).filter_by(deleted=False)


def add_category(category_name: str) -> int:
    """Add new category.

    :param category_name: string contains category name
    :return: a id of new category
    """
    category = CategoryModel()
    category.name = category_name
    category.save()

    return category.id
