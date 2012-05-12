# Copyright 2012 Aidan Skinner <aidan@skinner.me.uk>, all rights
# reserved

from votemap.model import Box, Candidate, PollingStation, Tally

def make_sample_data():
    michael = Candidate(name="Michael Shanks", party="Labour")
    michael.save()

    jordanhill_church = PollingStation(name="Jordan Hill Church",
                                       postcode="G13 1QT",
                                       coords=(55.88519010,
                                               4.329431899999999),
                                       min_box=236, max_box=239)
    tally = Tally(candidate=michael)
    tally.votes = [23,43,19,13,7,3,1,0,0,0,1,0,0]
    tally.save()
    jordanhill_church.save()
    box = Box(number=236, pollingstation=jordanhill_church)
    box.votes.append(tally)
    box.save()

    st_tams = PollingStation(name="St Thomas Aquinus",
                             postcode="G14 9PP",
                             coords=(55.88078530000001,
                                     -4.33564360),
                             min_box=240, max_box=241)
    st_tams.save()
    tally = Tally(candidate=michael)
    tally.votes = [20,56,22,12,5,4,1,0,1,0,0,0,0]
    tally.save()
    box = Box(number=240, pollingstation=jordanhill_church)
    box.votes.append(tally)
    box.save()
