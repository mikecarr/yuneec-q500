import geocoding_for_kml
import csv
import xml.dom.minidom
import sys
import fileinput
import getopt

# reference https://developers.google.com/kml/articles/csvtokml


def insert_line_num():
    print('process file')

def show_help():
    print('runme.py -i <inputfile>')


def createPlacemark(kmlDoc, row, order,line_number):
    # This creates a  element for a row of data.
    # A row is a dict.
    dataElement = kmlDoc.createElement('wpt')
    
    # Loop through the columns and create a  element for every field that has a value.
    for key in order:

        if row[key]:
            dataElement.setAttribute('lat', row['latitude'])
            dataElement.setAttribute('lon', row['longitude'])

    valueElement = kmlDoc.createElement('ele')
    dataElement.appendChild(valueElement)
    valueText = kmlDoc.createTextNode(row['altitude'])
    valueElement.appendChild(valueText)

    valueElement = kmlDoc.createElement('name')
    dataElement.appendChild(valueElement)
    valueText = kmlDoc.createTextNode('Position ' + str(line_number))
    valueElement.appendChild(valueText)

    print(dataElement.toxml())

    return dataElement

def createDocHeader(gpxDoc):
      #<?xml version="1.0"?>
  #<gpx creator="GPS Visualizer http://www.gpsvisualizer.com/" version="1.1" 
  #xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  #xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">

    gpxElement = gpxDoc.createElementNS('http://www.topografix.com/GPX/1/1', 'gpx')
    gpxElement.setAttribute('xmlns','http://www.topografix.com/GPX/1/1')
    gpxElement.setAttribute('version','1.1')
    gpxElement = gpxDoc.appendChild(gpxElement)
    
    trkElement = gpxDoc.createElement('trk')
    gpxElement.appendChild(trkElement)

    trksegElement = gpxDoc.createElement('trkseg')
    trkElement.appendChild(trksegElement)

    trkptElement = gpxDoc.createElement('trkpt')
    trkptElement.setAttribute('lat','32.963573' )
    trkptElement.setAttribute('lon', '-117.064606')
    trksegElement.appendChild(trkptElement)

    timeElement = gpxDoc.createElement('time')
    trkptElement.appendChild(timeElement)
    valueText = gpxDoc.createTextNode('2015-07-14T20:04:31Z')
    timeElement.appendChild(valueText)

    metaElement = gpxDoc.createElement('meta')
    gpxElement.appendChild(metaElement)
    valueText = gpxDoc.createTextNode('Created by my python script for Q500+ flightlogs')
    metaElement.appendChild(valueText)
    return gpxElement


def createGPX(csvReader, fileName, order):
    # This constructs the KML document from the CSV file.
    gpxDoc = xml.dom.minidom.Document()
    gpxElement = createDocHeader(gpxDoc)

    line_number = 1

    # Skip the header line.
    next(csvReader)

    for row in csvReader:
        placemarkElement = createPlacemark(gpxDoc, row, order, line_number)
        #print(placemarkElement.toprettyxml)
        gpxElement.appendChild(placemarkElement)
        line_number += 1

    kmlFile = open(fileName, 'w')
    #kmlFile.write(gpxDoc.toprettyxml('  ', newl = '\n', encoding = 'utf-8'))
    kmlFile.write(gpxDoc.toxml())

def createKML(csvReader, fileName):
    # This constructs the KML document from the CSV file.
    kmlDoc = xml.dom.minidom.Document()
  
    kmlElement = kmlDoc.createElementNS('http://earth.google.com/kml/2.2', 'kml')
    kmlElement.setAttribute('xmlns','http://earth.google.com/kml/2.2')
    kmlElement = kmlDoc.appendChild(kmlElement)
    documentElement = kmlDoc.createElement('Document')
    documentElement = kmlElement.appendChild(documentElement)

    # Skip the header line.
    next(csvReader)

    for row in csvReader:
        placemarkElement = createPlacemark(kmlDoc, row, order)
        documentElement.appendChild(placemarkElement)
    kmlFile = open(fileName, 'w')
    kmlFile.write(kmlDoc.toprettyxml('  ', newl = '\n', encoding = 'utf-8'))

def main(argv):
    print('Hello')
    inputfile = ''
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
            inputfile = arg

    print('Input file is ', inputfile)

    csvreader = csv.DictReader(open(inputfile))
    order = ['latitude','longitude', 'altitude']

    if map_type == 'kml':
        kml = createKML(csvreader, 'flightlog.kml', order)
    elif map_type == 'gpx':
        kml = createGPX(csvreader, 'flightlog.gpx', order)

if __name__ == '__main__':
    main(sys.argv[1:])
