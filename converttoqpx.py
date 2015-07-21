import csv
import xml.dom.minidom
import sys
import fileinput
import getopt
import datetime,time


# reference https://developers.google.com/kml/articles/csvtokml

# define globals
last_date = ''
last_lat = ''
last_long = ''

def insert_line_num():
    print('process file')

def show_help():
    print('runme.py -i <inputfile>')


def footToMeter(foot):
    return foot * .305

def datetime_to_utc(date):
    """Returns date in UTC w/o tzinfo"""
    return date.astimezone(tz.gettz('UTC')).replace(tzinfo=None) if date.tzinfo else date

def createTrack(kmlDoc, row, order,line_number):

    global last_lat, last_long, last_date
    
    # This creates a  element for a row of data.
    # A row is a dict.
    dataElement = kmlDoc.createElement('trkpt')
    
    # Loop through the columns and create a  element for every field that has a value.
    for key in order:

        if row[key]:
            latitude = row['latitude']
            longitude = row['longitude']

            # cleanup bogus data
            if latitude == '0.0' or longitude == '0.0':
                return None

            #print("Last Lat: " + last_lat + ", latitude:" + latitude)
            #print("Last Long: " + last_long + ", longitude:" + longitude)
            #print("XXXX")

            # cleanup duplicates
            if latitude == last_lat and longitude == last_long:
                return None

            dataElement.setAttribute('lat', latitude)
            dataElement.setAttribute('lon', longitude)

    last_lat = latitude
    last_long = longitude

    # elevation
    valueElement = kmlDoc.createElement('ele')
    dataElement.appendChild(valueElement)
    alt = float(row['altitude'])

    # set negative values to 0.0
    if alt < 0:
        alt = 0.0

    valueText = kmlDoc.createTextNode(str(alt))
    valueElement.appendChild(valueText)

    # date/time needs to be in UTC
    dt = datetime.datetime.strptime(row[''], '%Y%m%d %H:%M:%S:%f')
    #print(row[''])

    # removes any duplicate dates entries
    if dt == last_date:
        return None

    last_date = dt
    zt = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.mktime(dt.timetuple())))

    valueElement = kmlDoc.createElement('time')
    dataElement.appendChild(valueElement)
    valueText = kmlDoc.createTextNode(str(zt))
    valueElement.appendChild(valueText)

    # print out for debugging
    print(dataElement.toxml())

    return dataElement


def createTrackDocHeader(gpxDoc):

    gpxElement = gpxDoc.createElementNS('http://www.topografix.com/GPX/1/1', 'gpx')
    gpxElement.setAttribute('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
    gpxElement.setAttribute('creator','Mike Carr, My custom python script')
    gpxElement.setAttribute('xmlns','http://www.topografix.com/GPX/1/1')
    gpxElement.setAttribute('version','1.1')
    
    gpxElement = gpxDoc.appendChild(gpxElement)

    # metaElement = gpxDoc.createElement('metadata')
    # gpxElement.appendChild(metaElement)
    # valueText = gpxDoc.createTextNode('Created by my python script for Q500+ flightlogs')
    # metaElement.appendChild(valueText)

    trkElement = gpxDoc.createElement('trk')
    gpxElement.appendChild(trkElement)

    trksegElement = gpxDoc.createElement('name')
    trkElement.appendChild(trksegElement)
    valueText = gpxDoc.createTextNode('Q500')
    trksegElement.appendChild(valueText)
    trkElement.appendChild(trksegElement)
    
    return trkElement


def createGPXTrack(csvReader, fileName, order):

    # This constructs the KML document from the CSV file.
    gpxDoc = xml.dom.minidom.Document()
    gpxElement = createTrackDocHeader(gpxDoc)

    line_number = 1

    # Skip the header line.
    next(csvReader)

    trksegElement = gpxDoc.createElement('trkseg')
    gpxElement.appendChild(trksegElement)

    for row in csvReader:
        placemarkElement = createTrack(gpxDoc, row, order, line_number)

        #print(placemarkElement.toprettyxml)
        if placemarkElement != None:
            trksegElement.appendChild(placemarkElement)
            line_number += 1

    kmlFile = open(fileName, 'w')
    kmlFile.write(gpxDoc.toprettyxml('  ', newl = '\n', encoding = 'utf-8'))

def createDashFile(csvReader, fileName, order):
    print('creating dash file')

def main(argv):
    print('Hello, welcome to Q500 FlightLog Converter!')
    input_file = ''
    output_file = 'flightlog.gpx'
    map_type = ''

    try:
        opts, args = getopt.getopt(argv,"hi:o:t:",["ifile=","ofile="])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            show_help()
            sys.exit()
        elif opt in ("-t", "--type"):
            map_type = arg
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg

    print('Input file is ', input_file)

    csvreader = csv.DictReader(open(input_file))
    order = ['','latitude','longitude', 'altitude']

    if map_type == 'gpx':
        createGPXTrack(csvreader, output_file, order)
    elif map_type == 'dash':
        createDashFile(csvreader, output_file, order)

if __name__ == '__main__':
    main(sys.argv[1:])
