#!/usr/bin/python3
"""Place objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = [place.to_dict() for place in city.places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    """Retrieves a place by it id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates place object through city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, description="Missing user_id")
    if "name" not in request.get_json():
        abort(400, description="Missing name")
    place_data = request.get_json()
    user = storage.get(User, place_data['user_id'])
    if user is None:
        abort(404)
    place_data['city_id'] = city.id
    place_data['user_id'] = user.id
    place = Place(**place_data)
    place.save()
    return jsonify(place)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update place"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_data = request.get_json()
    to_ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated']
    for key, value in place_data:
        if key not in to_ignore:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict())
