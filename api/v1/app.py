#!/usr/bin/python3
"""Status of your API"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(exception):
    """closes db session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """return error page not found"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    app.run(host=os.getenv("HBNB_API_HOST", "0.0.0.0"),
            port=os.getenv("HBNB_API_PORT", "5000"), threaded=True)
