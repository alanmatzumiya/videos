# -*- coding: utf-8 -*-

from flask import Blueprint, abort, jsonify
container = Blueprint("container",  __name__)


@container.route("/container/")
@container.route("/container/videos/")
@container.route("/container/videos/<container_name>/")
def container_view(container_name=None):
    data = dict(container_name=container_name)
    if container_name:
        return jsonify(data)
    else:
        return abort(404)
