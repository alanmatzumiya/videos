# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, jsonify, abort
from .build import Template, WaitingFiles, RejectedFiles
home = Blueprint(
    "home",
    __name__,
    template_folder=Template.folder,
    static_folder=Template.static
)


@home.route("/", methods=["GET"])
def home_view():
    return render_template(
        "index.html",
        static=home.static_url_path
    )


@home.route("/get-data/", methods=["GET"])
@home.route("/get-data/<folder_name>/", methods=["GET"])
def get_folder_data(folder_name=None):
    folder = dict(
        waiting=WaitingFiles,
        rejected=RejectedFiles
    ).get(folder_name)
    if folder:
        datafolder = folder().files
        return jsonify(datafolder)
    else:
        abort(404)


@home.route("/api/get/", methods=["GET"])
@home.route("/api/get/<opt>/", methods=["GET"])
def api_get(opt=None):
    if opt:
        print(opt)
    return jsonify(Template.get_request())


@home.route("/api/post/", methods=["GET", "POST"])
@home.route("/api/post/<opt>/", methods=["GET", "POST"])
def api_post(opt=None):
    if opt == "update":
        return Template.send_json(dict(
            response_from="all data has been updated successfully"
        ))
    else:
        return abort(404)
