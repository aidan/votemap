# Copyright 2012 Aidan Skinner <aidan@skinner.me.uk>, all rights
# reserved

from flask import Blueprint, jsonify, render_template, request
from shapely.geometry import MultiPoint

from votemap.model import Candidate, PollingStation

controllers = Blueprint("controllers", __name__,
                        static_folder="static")

@controllers.route("/", methods=["GET"])
def index():
    candidates = Candidate.objects.all()
    polling_stations = PollingStation.objects.order_by("name").all()
    stations = {}
    for candidate in candidates:
        stations[candidate.id] = {}
        total = 0
        for ps in polling_stations:
            try:
                stations[candidate.id][ps.name] = ps.get_total_for_candidate(str(candidate.id))
                total = total + stations[candidate.id][ps.name]
            except:
                # skip it
                pass
        stations[candidate.id]["total"] = total
    return render_template("index.html", candidates=candidates, stations=stations)

@controllers.route("map", methods=["GET"])
def map():
    candidate_id = request.args["candidate_id"]
    return render_template("map.html", candidate_id=candidate_id)

@controllers.route('get_candidate_data')
def get_candidate_data():
    candidate_id = request.args["candidate_id"]
    data = []
    polling_stations = PollingStation.objects.all()
    geoms = []
    for ps in polling_stations:
        total = ps.get_total_for_candidate(candidate_id)
        geoms.append(ps.coords)
        lat, lon = ps.coords
        data.append({"name": ps.name,
                     "lat": lat,
                     "lon": lon,
                     "total": total,
                     "percentage": int((float(total) / ps.get_total_votes()) * 100)
                     })
    area = MultiPoint(geoms)
    viewdata = {"centre_lat": area.centroid.x,
                "centre_lon": area.centroid.y}
                  
    return jsonify(results=data, viewdata=viewdata)
