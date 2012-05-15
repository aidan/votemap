from optparse import OptionParser

from votemap.app import create_app
from votemap.import_data import import_polling_stations, import_boxes
from votemap.model import clear_collections

if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-p", "--polling-stations",
                      dest="polling_station", default=False,
                      help="Polling station file to import")

    parser.add_option("-b", "--boxes",
                      dest="boxes", default=False,
                      help="Box report file to import")

    (options, args) = parser.parse_args()
    
    app = create_app()
    clear_collections()
    import_polling_stations(options.polling_station)
    import_boxes(options.boxes)
