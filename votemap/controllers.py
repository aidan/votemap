# Copyright 2012 Aidan Skinner <aidan@skinner.me.uk>, all rights
# reserved

from flask import Blueprint, jsonify, render_template, request
from shapely.geometry import MultiPoint

from votemap.model import Candidate, PollingStation, Ward

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
    data = []
    polling_stations = PollingStation.objects.all()
    geoms = []
    for ps in polling_stations:
        total = ps.get_total_for_candidate(candidate_id, preference)
        if total == 0:
            continue
        geoms.append(ps.coords)
        lat, lon = ps.coords
        data.append({"id": str(ps.id),
                     "name": ps.name,
                     "lat": lat,
                     "lon": lon,
                     "votes":
                         { "total": total,
                           "percentage": int((float(total) /
                                              ps.get_total_votes(preference)) * 100)
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
