# Copyright 2012 Aidan Skinner <aidan@skinner.me.uk>, all rights
# reserved

from flaskext.mongoengine import MongoEngine

from mongoengine.queryset import QuerySet

db = MongoEngine()

class PollingStation(db.Document):
    name = db.StringField(required=True, unique=True)
    postcode = db.StringField(required=True, unique=True)
    ne_coords = db.GeoPointField()
    sw_coords = db.GeoPointField()
    min_box = db.IntField(required=True, unique=True)
    max_box = db.IntField(required=True, unique=True)

    @classmethod
    def get_by_name(cls, name):
        return cls.objects(name=name).first()

    @classmethod
    def get_for_box(cls, box_number):
        return cls.objects(min_box__lte=box_number, max_box__gte=box_number).first()
    
class Candidate(db.Document):
    """
    A candidate who gets votes
    """

    name = db.StringField(required=True, unique=True)
    party = db.StringField()

class Tally(db.Document):
    candidate = db.ReferenceField(Candidate)
    preferences = db.ListField()
    
class Box(db.Document):
    number = db.IntField(required=True, unique=True)
    polling_station = db.ReferenceField(PollingStation, required=True)
    votes = db.ListField()

    @classmethod
    def get_by_polling_station(cls, ps):
        return cls.objects(polling_station=ps).all()

def clear_collections():
    PollingStation.drop_collection()
    Candidate.drop_collection()
    Tally.drop_collection()
    Box.drop_collection()
    # mongoengine records which indexes have already been created, but
    # fails to reset the state when the collection is dropped.
    QuerySet._reset_already_indexed()
    
