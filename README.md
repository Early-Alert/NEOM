# NEOM
automate.sh is a bash script that can be set up to run under cron, and executes 4 python scripts:

datea.py, (get current date amd wget data)
wavesauto.py, (extract, interpolate, and generate geojson from grib2 data)
uploadWWdayn.py (uploads geojson to portal)
