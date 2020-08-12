"""Views from api v1.
"""
# api.add_resource(SpotSearch, '/spots/<string:name>')
# api.add_resource(SpotList, '/spots/<int:page>')
# api.add_resource(SpotAdd, '/spots')
# api.add_resource(CategoryAdd, '/categories')
# api.add_resource(PictureAdd, '/pictures')
# api.add_resource(PictureDelete, '/pictures/<int:picture_id>')
# api.add_resource(FavoriteList, '/favorites/<int:user_id>')
# api.add_resource(FavoriteAdd, '/favorites')
# api.add_resource(FavoriteDelete, '/favorites/<int:favorite_id>')
from typing import Any, Tuple

from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required
from sqlalchemy.exc import IntegrityError

from snowman_challenge import logic

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')


@blueprint.route('/user', methods=['POST'])
def add_user() -> Tuple[Any, int]:
    """Add user.

    :return: a tuple of response
    """
    username = request.json.get('username')
    password = request.json.get('password')
    logic.add_user(username, password)
    return jsonify({}), 200


@blueprint.route('/spots/<int:page>', methods=['GET'])
def spot_list(page: int = 1) -> Tuple[Any, int]:
    """Retrieve a list of spots.

    :param page: number of page
    :return: A tuple of response
    """
    return jsonify(logic.get_spot_list(page)), 200


@blueprint.route('/spots', methods=['POST'])
@jwt_required()
def spot_add() -> Tuple[Any, int]:
    """Register new spot.

    :return: Response tuple.
    """
    spot_data = request.json
    try:
        logic.register_spot(spot_data)
    except IntegrityError:
        status = 409
        response_data = {
            'msg': 'Spot is already added!',
        }
    else:
        status = 201
        response_data = {
            'msg': 'Spot sucessully added',
        }

    return response_data, status


@blueprint.route('/spots/<string:name>', methods=['GET'])
def spot_search(name: str) -> Tuple[Any, int]:
    """Search spot by name.

    :param name: name of spot to search
    :return: A tuple with response object
    """
    spot_data = logic.search_spot_by_name(name)
    if len(spot_data) <= 0:
        return jsonify(spot_data), 404

    return jsonify(spot_data), 200


@blueprint.route('/categories', methods=['POST'])
@jwt_required()
def category_add() -> Tuple[Any, int]:
    """Endpoint for add category.

    :return: response tuple
    """
    response_data = {}
    name = request.json.get('name')
    try:
        logic.add_category(category_name=name)
    except IntegrityError:
        status = 409
        response_data = {
            'msg': 'Category is already added!',
        }
    else:
        status = 201
        response_data = {
            'msg': 'Category added succesfully!',
        }
    finally:
        response = jsonify(response_data), status

    return response


@blueprint.route('/pictures', methods=['POST'])
@jwt_required()
def picture_add() -> Tuple[Any, int]:
    """Add pictures to spot.

    :return: response tuple
    """
    spot_id = request.json.get('spot_id')
    filename = request.json.get('filename')
    try:
        logic.add_picture(spot_id, filename)
    except IntegrityError:
        status = 409
        response_data = {
            'msg': 'Picture is already added!',
        }
    else:
        status = 201
        response_data = {
            'msg': 'Picture added succesfully',
        }
    finally:
        response = jsonify(response_data), status

    return response


@blueprint.route('/picture/<int:picture_id>', methods=['DELETE'])
@jwt_required()
def picture_delete(picture_id: int) -> Tuple[Any, int]:
    """Delete picture.

    :param picture_id: id of picture
    :return: a tuple with response
    """
    logic.remove_picture(picture_id)
    status = 200
    response_data = {
        'msg': 'Picture successful deleted!',
    }
    return jsonify(response_data), status


@blueprint.route('/favorite/<int:user_id>', methods=['GET'])
@jwt_required()
def favorite_list(user_id: int) -> Tuple[Any, int]:
    """Get favorite list.

    :param user_id: user id of favorite list
    :return: a tuple with response
    """
    response_data = logic.list_favorites_spots(user_id)
    return jsonify(response_data), 200


@blueprint.route('/favorite', methods=['POST'])
@jwt_required()
def favorite_add() -> Tuple[Any, int]:
    """Include new spot on favorite.

    :return: a tuple with response
    """
    user_id = request.json.get('user_id')
    spot_id = request.json.get('spot_id')
    try:
        logic.add_to_favorites(user_id, spot_id)
    except IntegrityError:
        status = 409
        response_data = {
            'msg': 'The item is already on favorite list!',
        }

    else:
        status = 201
        response_data = {
            'msg': 'Spot was included on favorites sucessully!',
        }

    return jsonify(response_data), status


@blueprint.route('/favorite/<int:favorite_id>', methods=['DELETE'])
@jwt_required()
def favorite_delete(favorite_id: int) -> Tuple[Any, int]:
    """Delete favorite.

    :param favorite_id: id of favorite list
    :return: a tuple with response
    """
    logic.remove_from_favorites(favorite_id)
    status = 200
    response_data = {
        'The favorite was removed succesfully',
    }

    return jsonify(response_data), status
