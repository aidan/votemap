# Copyright 2012 Aidan Skinner <aidan@skinner.me.uk>, all rights
# reserved

from votemap.model import Box, Candidate, PollingStation, Tally

def make_sample_data():
    michael = Candidate(name="Michael Shanks", party="Labour")
    michael.save()
    aileen = Candidate(name="Aileen Colleran", party="Labour")
    aileen.save()

    
    jordanhill_church = PollingStation(name="Jordan Hill Church",
                                       postcode="G13 1QT",
                                       ne_coords=(55.88564250,
                                                  -4.32859980),
                                       sw_coords=(55.88461760,
                                                  -4.33007750),
                                       min_box=236, max_box=239)
    jordanhill_church.save()
    
    box = Box(number=236, polling_station=jordanhill_church)
    tally = Tally(candidate=michael)
    tally.preferences = [23,43,19,13,7,3,1,0,0,0,1,0,0]
    tally.save()
    box.votes.append(tally)
    tally = Tally(candidate=aileen)
    tally.preferences = [56,37,21,18,4,3,1,0,0,0,0,0,1]
    tally.save()
    box.votes.append(tally)
    box.save()

    st_tams = PollingStation(name="St Thomas Aquinus",
                             postcode="G14 9PP",
                             ne_coords=(55.88139160,
                                        -4.33425780),
                             sw_coords=(55.88030260,
                                        -4.337324499999999),
                             min_box=240, max_box=241)
    st_tams.save()
    tally = Tally(candidate=michael)
    tally.preferences = [20,56,22,12,5,4,1,0,1,0,0,0,0]
    tally.save()
    box = Box(number=240, polling_station=st_tams)
    box.votes.append(tally)
    tally = Tally(candidate=aileen)
    tally.preferences = [45,53,28,15,8,1,2,0,0,0,0,0,2]
    tally.save()
    box.votes.append(tally)
    box.save()
