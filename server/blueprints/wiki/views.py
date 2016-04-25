from flask import Blueprint, render_template, abort, jsonify
from utils import pathfinder

import json

blueprint = Blueprint("wiki", __name__, url_prefix="/wiki")

@blueprint.route('/<one>/<two>')
def display_paths(one, two, depth=3):
    if not (one and two):
        abort(404), "You must enter two search terms."

    routes = pathfinder(one, two, depth)
    if routes:
        return jsonify(paths=routes)
    else:
        abort(404), "Article not found!"
