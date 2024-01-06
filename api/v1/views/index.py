#!/usr/bin/python3

"""API views"""

from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Return json response status as json object"""
    status = {
        'status': 'OK'
    }
    return jsonify(status)


@app_views.route('/stats')
def stats():
    """Retrieves number of each objects by type"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
