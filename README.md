# Runme.py (better name to come :-))
Python script to convert Yuneec Q500+ Flight logs into GPX format. This file can then be uploaded to http://www.doarama.com/ for a visual representation of your flight.

## Running

````
python converttoqpx.py -i <flightlog file> -t gpx [ -o <output filename> ]
````
This will create a file named fightlog.gpx, navigate to http://www.doarama.com/ and load GPX file, enjoy!

## Debugging
drop a gpx file here http://nationalmap.gov.au/

## References
* https://developers.google.com/kml/articles/csvtokml
* http://www.doarama.com/api/0.2/docs
* http://www.rigacci.org/wiki/doku.php/tecnica/gps_cartografia_gis/gpx
