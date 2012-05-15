# Copyright 2012 Aidan Skinner <aidan@skinner.me.uk>, all rights
# reserved

import urllib

from flask import Blueprint, render_template, request

from votemap.model import Box, Candidate, PollingStation

controllers = Blueprint("controllers", __name__,
                        static_folder="static")

@controllers.route("/", methods=["GET"])
def index():
    candidates = Candidate.objects.all()
    return render_template("index.html", candidates=candidates)

@controllers.route("map", methods=["GET"])
def map():
    candidate_id = request.args["candidate_id"]
    data = []
    polling_stations = PollingStation.objects.all()
    for ps in polling_stations:
        total = 0
        for box in Box.get_by_polling_station(ps):
            for tally in box.votes:
                if str(tally.candidate.id) == candidate_id:
                    total = total + tally.preferences[0]
        for coords in ps.ne_coords, ps.sw_coords:
            a, b = coords
            data.append('%s %s %d' % (a, b, total))

    print '\n'.join(data)
    params = urllib.urlencode({'thedata': '\n'.join(data),
                               'xresInput':20,
                               'yresInput':20,
                               'lowercutoffInput':0.1,
                               'blendInput':20,
                               'xsizeInput':800,
                               'ysizeInput':600,
                               'zoomInput':14
                               })
    f = urllib.urlopen('http://diffent.com/map/mapit10.php',
                       params)
        
    return f.read()
