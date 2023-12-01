# -*- coding: utf-8 -*-

from flask import Blueprint, abort, jsonify, redirect, url_for
from pathlib import Path
youtube = Blueprint("youtube",  __name__)
path = Path(__file__).parent


@youtube.route("/youtube/")
@youtube.route("/youtube/<opt>/")
def yt_view(opt=None):
    if opt in ("get-data", "get-download"):
        return redirect(url_for(opt))
    else:
        return abort(404)


@youtube.route("/youtube/get-data/")
def yt_data():
    return jsonify(video_id="")


@youtube.route("/youtube/get-download/")
def yt_download():
    return jsonify(video_id="", video_title="")
