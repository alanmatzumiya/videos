# -*- coding: utf-8 -*-

from subprocess import getoutput as getout
from pathlib import Path
apath = Path(__file__).parent
host = getout("hostname -I").split()[-1]
port = 5050
url = f"http://{host}:{port}"
import_name = "app"
template_folder = "./templates"
config = dict(
    ENV="development",
    SECRET_KEY="alanmatzumiya",
    SESSION_TYPE="filesystem"
)
deployment_settings = dict(
    use_reloader=True,
    use_debugger=True,
    use_evalex=True
)
dataset = {
    x: globals().get(x)
    for x in dir()
    if not x.startswith("__")
}
