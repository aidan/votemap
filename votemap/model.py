# Copyright 2012 Aidan Skinner <aidan@skinner.me.uk>, all rights
# reserved

from flaskext.mongoengine import MongoEngine
from mongoengine import signals

db = MongoEngine()

class PollingStation(db.Document):
    name = db.StringField()
    postcode = db.StringField()
    coords = db.GeoPointField()

class Candidate(db.Document):
    """
    A candidate who gets votes
    """

    name = db.StringField()
    party = db.StringField()
