from optparse import OptionParser
import os

from votemap.app import create_app
from votemap.import_data import import_boxes, import_candidates, import_polling_stations
from votemap.model import clear_collections

if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-p", "--polling-stations",
                      dest="polling_station", default=False,
                      help="Polling station file to import")

    parser.add_option("-b", "--boxes",
                      dest="boxes", default=False,
                      help="Directory with boxes to import")

    parser.add_option("-n", "--notice",
                      dest="notice", default=False,
                      help="Text notice of poll")

    (options, args) = parser.parse_args()
    
    app = create_app()
    clear_collections()
    if options.notice:
        import_candidates(options.notice)
    if options.polling_station:
        import_polling_stations(options.polling_station)
    if options.boxes:
        for boxfile in os.listdir(options.boxes):
            print boxfile
            import_boxes(options.boxes+"/"+boxfile)
