"""Resources from API v1.
"""

from typing import List, Tuple, Any

from flask import jsonify, request
from flask_jwt import jwt_required
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from snowman_challenge.api.v1 import api
# from snowman_challenge import consts
from snowman_challenge import logic


class SpotList(Resource):
    """SpotList endpoint.
    """

    def get(self, page: int = 1) -> Tuple[Any, int]:
        """Retrieve a list of spots.

        :param page: number of page
        :return: A tuple of response
        """
        return jsonify(logic.get_spot_list(page)), 200


class SpotAdd(Resource):
    """SpotAdd endpoint."""

    @jwt_required()
    def post(self) -> Tuple[Any, int]:
        """Register new spot.

        :return: Response tuple.
        """
        spot_data = request.json()
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


class SpotSearch(Resource):
    """Spot search endpoint.
    """

    def get(self, name: str) -> Tuple[Any, int]:
        """Search spot by name.

        :param name: name of spot to search
        :return: A tuple with response object
        """
        spot_data = logic.search_spot_by_name(name)
        if len(spot_data) <= 0:
            return jsonify(spot_data), 404

        return jsonify(spot_data), 200


class CategoryAdd(Resource):
    """CategoryAdd endpoint.
    """

    @jwt_required()
    def post(self) -> Tuple[Any, int]:
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


class PictureAdd(Resource):
    """PictureAdd endpoint.
    """

    @jwt_required()
    def post(self) -> Tuple[Any, int]:
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


class PictureDelete(Resource):
    """PictureDelete endpoint.
    """

    @jwt_required()
    def delete(self, picture_id: int) -> Tuple[Any, int]:
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


class FavoriteList(Resource):
    """FavoriteList endpoint.
    """

    @jwt_required()
    def get(self, user_id: int) -> Tuple[Any, int]:
        """Get favorite list.

        :param user_id: user id of favorite list
        :return: a tuple with response
        """
        response_data = logic.list_favorites_spots(user_id)
        return jsonify(response_data), 200


class FavoriteAdd(Resource):
    """FavoriteAdd endpoint.
    """

    @jwt_required()
    def post(self) -> Tuple[Any, int]:
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


class FavoriteDelete(Resource):
    """FavoriteDelete endpoint."""

    @jwt_required()
    def delete(self, favorite_id: int) -> Tuple[Any, int]:
        """Delete favorite.

        :param favorite_id: id of favorite list
        """
        logic.remove_from_favorites(favorite_id)
        status = 200
        response_data = {
            'The favorite was removed succesfully',
        }

        return jsonify(response_data), status


api.add_resource(SpotSearch, '/spots/<string:name>')
api.add_resource(SpotList, '/spots/<int:page>')
api.add_resource(SpotAdd, '/spots')
api.add_resource(CategoryAdd, '/categories')
api.add_resource(PictureAdd, '/pictures')
api.add_resource(PictureDelete, '/pictures/<int:picture_id>')
api.add_resource(FavoriteList, '/favorites/<int:user_id>')
api.add_resource(FavoriteAdd, '/favorites')
api.add_resource(FavoriteDelete, '/favorites/<int:favorite_id>')
