# Copyright 2012 Aidan Skinner <aidan@skinner.me.uk>, all rights
# reserved

import csv
import re

from votemap.model import Box, Candidate, PollingStation, Tally

def import_polling_stations(pspath):
    ps_reader = csv.reader(open(pspath, 'rb'))
    
    # Skip header row
    ps_reader.next()
    count = 0
    print ("Started with %d Polling Stations" % (PollingStation.objects.count()))
    for row in ps_reader:
        address = re.sub('\xc2\xa0', ' ', row[0])
        boxes = row[1]
        ps = PollingStation()

        ps.postcode = ("%s %s" % (address.split(' ')[-2], address.split(' ')[-1]))
        ps.name = address.split(',')[0]

        if boxes.find(' ') > 0:
            box_bits = boxes.split(' ')
            ps.min_box = int(box_bits[0])
            ps.max_box = int(box_bits[2])
        else:
            ps.min_box = int(boxes)
            ps.max_box = int(boxes)

        ps.save()
        count = count + 1
    print ("Added %d Polling Stations to finish with %d" %
           (count, PollingStation.objects.count()))

def import_boxes(boxpath):
    print ("Started with %d Boxes" % (Box.objects.count()))
    box_reader = csv.reader(open(boxpath, 'rb'))
    box = None
    in_box = False
    count = 0 
    for row in box_reader:
        if re.match('^BOX', row[0]):
            in_box = True
            box = Box()
            box.number = row[0].split(' ')[1]
            box.polling_station = PollingStation.get_for_box(box.number)
            count = count + 1
        elif in_box:
            name = row[0]
            candidate = Candidate.get_by_name(name)
            if candidate is None:
                candidate = Candidate(name=name)
                candidate.save()
            tally = Tally(candidate=candidate)
            try:
                tally.preferences = [int(i) for i in row[1:]]
            except ValueError:
                pass # preference header row
            tally.save()
            box.votes.append(tally)
            box.save()

    print ("Added %d boxes to finish with %d" %
           (count, Box.objects.count()))
            
            
            
            
