# Copyright 2012 Aidan Skinner <aidan@skinner.me.uk>, all rights
# reserved

from flask import Blueprint, jsonify, render_template, request
from shapely.geometry import MultiPoint

from votemap.model import Candidate, PollingStation, Tally, Ward

controllers = Blueprint("controllers", __name__,
                        static_folder="static")

@controllers.route("/", methods=["GET"])
def index():
    return render_template("index.html", wards=Ward.objects.all())

@controllers.route("map", methods=["GET"])
def map():
    candidate_id = request.args["candidate_id"]
    return render_template("map.html", candidate_id=candidate_id)

@controllers.route('get_candidate_data')
def get_candidate_data():
    candidate_id = request.args["candidate_id"]
    preference = int(request.args["preference"])
    geoms = []
    ps = {}
    candidate = Candidate.objects(id=candidate_id).first()
    if candidate is None:
        return
    tallies = Tally.objects(candidate=candidate).all()
    for tally in tallies:
        p = tally.polling_station.id
        if p not in ps:
            ps[p] = tally.preferences[preference]
        else:
            ps[p] += tally.preferences[preference]
        
    data = []
    for p_id, total in ps.items():
        p = PollingStation.objects(id=p_id).first()
        geoms.append(p.coords)
        lat, lon = p.coords
        data.append({"id": str(p.id),
                     "name": p.name,
                     "lat": lat,
                     "lon": lon,
                     "votes":
                         { "total": total,
                           "percentage": int((float(total) /
                                              p.get_total_votes(preference)) * 100)
                           }
                     })
    area = MultiPoint(geoms)
    viewdata = {"centre_lat": area.centroid.x,
                "centre_lon": area.centroid.y}
                  
    return jsonify(results=data, viewdata=viewdata)

@controllers.route('get_ward_data')
def get_ward_data():
    ward_id = request.args["ward"]
    ward = Ward.objects(id=ward_id).first()
    candidate_data = []
    for c in ward.get_candidates():
        candidate_data.append({"id": str(c.id),
                               "name": c.name
                               })
    polling_station_data = []
    for p in ward.get_polling_stations():
        polling_station_data.append({"id": str(p.id),
                                     "name": p.name
                                     })
    return jsonify(candidates=candidate_data, polling_stations=polling_station_data)
