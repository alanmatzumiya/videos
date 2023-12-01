# -*- coding: utf-8 -*-

from flask import Blueprint
from .build import Template
dispatcher = Blueprint("dispatcher", __name__)


@dispatcher.route("/", methods=["GET", "POST"])
def dispatcher_view():
    return Template.send_json(dict(response_from="dispatcher"))
