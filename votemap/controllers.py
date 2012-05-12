# Copyright 2012 Aidan Skinner <aidan@skinner.me.uk>, all rights
# reserved

from flask import Blueprint, flash, render_template, redirect, request, url_for
from mongoengine import Q

from votemap.model import Candidate, PollingStation

controllers = Blueprint("controllers", __name__,
                        static_folder="static")

@controllers.route("/", methods=["GET"])
def index():
    return render_template("index.html")
