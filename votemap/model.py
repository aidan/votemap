# Copyright 2012 Aidan Skinner <aidan@skinner.me.uk>, all rights
# reserved

import json
import time
import urllib

from flask import current_app
from flaskext.mongoengine import MongoEngine

from mongoengine.queryset import QuerySet

db = MongoEngine()

class Ward(db.Document):
    number = db.IntField(required=True, unique=True)
    name = db.StringField(required=True)

    @classmethod
    def ensure_ward(cls, name, number):
        ward = cls.objects(number=number).first()
        if ward is None:
            ward = Ward()
            ward.number = number
            ward.name = name
            ward.save()
        return ward
    
    def get_polling_stations(self):
        return PollingStation.objects(ward=self.id).all()

    def get_candidates(self):
        return Candidate.objects(ward=self.id).all()
    
class PollingStation(db.Document):
    name = db.StringField(required=True, unique=True)
    postcode = db.StringField(required=True, unique=True)
    coords = db.GeoPointField()
    min_box = db.IntField(required=True, unique=True)
    max_box = db.IntField(required=True, unique=True)
    ward = db.ReferenceField(Ward)

    @classmethod
    def get_by_name(cls, name):
        return cls.objects(name=name).first()

    @classmethod
    def get_by_postcode(cls, postcode):
        return cls.objects(postcode=postcode).first()
    
    @classmethod
    def get_for_box(cls, box_number):
        return cls.objects(min_box__lte=box_number, max_box__gte=box_number).first()

    def get_total_votes(self, preference):
        total = 0
        for box in Box.get_by_polling_station(self):
            for tally in box.votes:
                try:
                    total = total + tally.preferences[preference]
                except:
                    current_app.logger.error ("Box %s tally for %s failed " % (box.number, tally.candidate.name))
        return total
    
    def update_coords(self):
        try:
            url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % \
                urllib.quote(self.postcode)
            location = json.loads(urllib.urlopen(url).read())["results"][0]['geometry']['location']
        except IndexError:
            time.sleep(1)
            url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % \
                urllib.quote(self.postcode)
            location = json.loads(urllib.urlopen(url).read())["results"][0]['geometry']['location']
        self.coords = (location['lat'], location['lng'])

    def get_total_for_candidate(self, candidate_id, preference):
        total = 0
        for box in Box.get_by_polling_station(self):
            for tally in box.votes:
                if str(tally.candidate.id) == candidate_id:
                    total = total + tally.preferences[preference]
        return total
        
    
class Candidate(db.Document):
    """
    A candidate who gets votes
    """

    name = db.StringField(required=True, unique=True)
    party = db.StringField()
    ward = db.ReferenceField(Ward, required=True)

    @classmethod
    def ensure_candidate(cls, name, ward, party=None):
        candidate = cls.get_by_name(name)
        if candidate is None:
            candidate = Candidate(name=name, ward=ward, party=party)
            candidate.save()
        return candidate
    
    @classmethod
    def get_by_name(cls, name):
        return cls.objects(name=name).first()

    @classmethod
    def get_by_party(cls, party, ward):
        return cls.objects(party=party, ward=ward).all()

class Tally(db.Document):
    candidate = db.ReferenceField(Candidate, required=True)
    preferences = db.ListField()
    polling_station = db.ReferenceField(PollingStation, required=True)
    
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
    Ward.drop_collection()
    # mongoengine records which indexes have already been created, but
    # fails to reset the state when the collection is dropped.
    QuerySet._reset_already_indexed()
    
