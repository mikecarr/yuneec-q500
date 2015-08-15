# converttoqpx.py (better name to come :-))
Python script to convert Yuneec Q500+ Flight logs into GPX format. This file can then be uploaded to http://www.doarama.com/ for a visual representation of your flight.

## Running

````
python converttoqpx.py -i <flightlog file> -t gpx [ -o <output filename> ]
````

### Yuneec Video conversion (avc to mov)

Install ffmpeg with Brew tools (MAC)
```
$ brew install ffmpeg
```

```
$ cd <location of your avc files>
$ convert_video_files.sh
```

This will create a file named fightlog.gpx, navigate to http://www.doarama.com/ and load GPX file, enjoy!

## Virtualenv
It creates an environment that has its own installation directories, that doesn’t share libraries with other virtualenv environments (and optionally doesn’t access the globally installed libraries either).

https://virtualenv.pypa.io/en/latest/

## Debugging
drop a gpx file here http://nationalmap.gov.au/

## Visualization Sites
* http://www.doarama.com/
* http://www.gpsvisualizer.com/
* http://maplorer.com/view_gpx.html
* http://veloroutes.org/upload/ (slow)

## References
* https://developers.google.com/kml/articles/csvtokml
* http://www.doarama.com/api/0.2/docs
* http://www.rigacci.org/wiki/doku.php/tecnica/gps_cartografia_gis/gpx
