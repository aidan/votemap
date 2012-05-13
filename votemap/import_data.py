# Copyright 2012 Aidan Skinner <aidan@skinner.me.uk>, all rights
# reserved

import csv
import re

from votemap.model import PollingStation

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
