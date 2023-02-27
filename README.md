# NEOM
automate.sh is a bash script that can be set up to run under cron, and executes 4 python scripts:

datea.py, (get current date amd wget data)
wavesauto.py, (extract, interpolate, and generate Sig Wave geojson from grib2 data)
bwavesauto.py, (extract, interpolate, calculate, and generate Beaufort Scale geojson from grib2 data)
uploadWWdayn.py (uploads geojson to portal)


A requirements.txt file will be included for dependencies.  
Note that the automate.sh script switches environments.
