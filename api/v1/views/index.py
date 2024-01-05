#!/usr/bin/python3

"""API views"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Return json response status as json object"""
    status = {
        'status': 'OK'
    }
    return jsonify(status)
