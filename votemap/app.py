# Copyright 2012 Aidan Skinner <aidan@skinner.me.uk>, all rights
# reserved

import logging
import logging.config
import os

from flask import Flask

from votemap.model import db
from votemap.controllers import controllers

app = Flask("votemap", static_folder="../static")

def configure_app(app):
    db.init_app(app)

def create_app():
    app.config.from_object("votemap.settings")

    # This will be set in deployed environments
    if "VOTEMAP_CONFIG" in os.environ:
        app.config.from_envvar("VOTEMAP_CONFIG")
    if "LOGGING_CONF" in app.config \
            and os.path.exists(app.config["LOGGING_CONF"]):
        logging.config.fileConfig(app.config["LOGGING_CONF"])
    if "LOGGER_NAME" in app.config:
        logging.root.name = app.config["LOGGER_NAME"]

    configure_app(app)

    app.register_blueprint(controllers, url_prefix='/')

    app.secret_key = "fuckyeahsocialism"
    
    return app
