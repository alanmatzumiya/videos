# -*- coding: utf-8 -*-

from werkzeug.exceptions import HTTPException
from build import Server
from views.build import Template, request
server = Server()
app = server.app


@app.errorhandler(HTTPException)
def handle_exception(error):
    return Template().error404(error)


@app.route("/get-data/")
def getdata():
    req = request.args.to_dict()
    headers = dict(request.headers)
    config = dict(app.config)
    config.pop("PERMANENT_SESSION_LIFETIME")
    return Template.send_json(req, config=config, headers=headers)


if __name__ == "__main__":
    server.run()
