# Copyright 2012 Aidan Skinner <aidan@skinner.me.uk>, all rights
# reserved

import csv
import logging
import re
import time

from votemap.model import Box, Candidate, PollingStation, Tally, Ward

def import_polling_stations(pspath):
    ps_reader = csv.reader(open(pspath, 'rb'))
    
    # Skip header row
    ps_reader.next()
    ps_count = 0
    print ("Started with %d Polling Stations" % (PollingStation.objects.count()))
    print ("Started with %d Wards" % (Ward.objects.count()))
    ward = None
    ward_count = 0
    for row in ps_reader:
        m = re.match("^WARD ([0-9]+) [^A-Za-z]* (.*)", row[0])
        if m:
            ward = Ward()
            ward.number = m.group(1)
            ward.name = m.group(2)
            ward.save()
            ward_count = ward_count + 1
            print ("Adding ward %s - %s" % (ward.number, ward.name))
        elif re.match("^Polling Place and Address", row[0]) or \
                re.match("^TOTAL", row[0]) or len(row[0]) == 0:
            continue
        else:
            try:
                address = re.sub('\xc2\xa0', ' ', row[0])
                boxes = row[1]
                postcode = ("%s %s" % (address.split(' ')[-2], address.split(' ')[-1]))
                ps = PollingStation.get_by_postcode(postcode)
                if ps is None:
                    ps = PollingStation(ward=ward)
                    ps.postcode = postcode
                    ps.name = address.split(',')[0]
                    ps_count = ps_count + 1
                
                if boxes.find(' ') > 0:
                    box_bits = boxes.split(' ')
                    if ps.min_box is None:
                        ps.min_box = box_bits[0]
                    else:
                        ps.min_box = min(ps.min_box, int(box_bits[0]))
                    if ps.max_box is None:
                        ps.max_box = int(box_bits[2])
                    else:
                        ps.max_box = max(ps.max_box, int(box_bits[2]))
                else:
                    if ps.min_box is None:
                        ps.min_box = int(boxes)
                    else:
                        ps.min_box = min(ps.min_box, int(boxes))
                    if ps.max_box is None:
                        ps.max_box = boxes
                    else:
                        ps.max_box = max(ps.max_box, int(boxes))
                if ps_count % 7 == 0:
                    time.sleep(1)
                ps.update_coords()
                ps.save()
            except Exception:
                logging.exception ("failed to make polling station from %s" % (row[0]))
                continue
    print ("Added %d Polling Stations to finish with %d" %
           (ps_count, PollingStation.objects.count()))
    print ("Added %d Wards to finish with %d" %
           (ward_count, Ward.objects.count()))

def import_boxes(boxpath):
    print ("Started with %d Boxes" % (Box.objects.count()))
    box_reader = csv.reader(open(boxpath, 'rb'))
    box = None
    in_box = False
    count = 0 
    for row in box_reader:
        try:
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
                    candidate = Candidate(name=name, ward=box.polling_station.ward)
                    candidate.save()
                tally = Tally(candidate=candidate)
                try:
                    tally.preferences = [int(i) for i in row[1:]]
                except ValueError:
                    pass # preference header row
                tally.save()
                box.votes.append(tally)
                box.save()
        except Exception:
            logging.exception("Failed to process box %s " % (box.number))

    print ("Added %d boxes to finish with %d" %
           (count, Box.objects.count()))
            
            
            
            
