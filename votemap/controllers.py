# Copyright 2012 Aidan Skinner <aidan@skinner.me.uk>, all rights
# reserved

import urllib

from flask import Blueprint, render_template

from votemap.model import Candidate, PollingStation

controllers = Blueprint("controllers", __name__,
                        static_folder="static")

@controllers.route("/", methods=["GET"])
def index():
    candidates = Candidate.objects.all()
    return render_template("index.html", candidates=candidates)

@controllers.route("map", methods=["GET"])
def map():
    data = []
    polling_stations = PollingStation.objects.all()
    for ps in polling_stations:
        for coords in ps.ne_coords, ps.sw_coords:
            a, b = coords
            data.append('%s %s %d'% (a, b, 25 + 20 * len(data)))

    print '\n'.join(data)
    params = urllib.urlencode({'thedata': '\n'.join(data),
                               'xresInput':20,
                               'yresInput':20,
                               'lowercutoffInput':0.0,
                               'blendInput':7,
                               'xsizeInput':800,
                               'ysizeInput':600,
                               'zoomInput':14
                               })
    f = urllib.urlopen('http://diffent.com/map/mapit10.php',
                       params)
        
    return f.read()
