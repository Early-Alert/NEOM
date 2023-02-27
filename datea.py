import os
from os.path import exists
import pickle


date=os.popen("date +%Y%m%d%H ").read()
dayago=os.popen("date +%Y%m%d%H --date='1 day ago' ").read()

#https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.yyyymmdd/hh/wave/gridded/
#gfswave.t12z.global.0p16.fFFF.grib2


#2023022421039
#0123456789012
#date=str(date)
#print(dayago,date)
os.system("mv errflg.txt errflg.old")
os.system("cd /mnt/f/CAMS/WAVE")

dd0=dayago[6:8]
dd1=date[6:8]
mm0=dayago[4:6]
mm1=date[4:6]
yy0=dayago[0:4]
yy1=date[0:4]
file1="gfswave.t18z.global.0p16.f021.grib2"
hh=date[8:10]

os.system("wget --tries=15 -T 1 https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs."+yy1+mm1+dd1+"/18/wave/gridded/"+file1)
fff=18
if exists(file1)==0:

	file1="gfswave.t12z.global.0p16.f027.grib2"
	fff=12

	os.system("wget ---tries=15 -T 1 https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs."+yy1+mm1+dd1+"/12/wave/gridded/"+file1)	
	if exists(file1)==0:
		fff=6
		file1="gfswave.t06z.global.0p16.f033.grib2"
		os.system("wget --tries=15 -T 1 https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs."+yy1+mm1+dd1+"/06/wave/gridded/"+file1)
		if exists(file1)==0:
			fff=0
			file1="gfswave.t00z.global.0p16.f039.grib2"
			os.system("wget --tries=15 -T 1 https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs."+yy1+mm1+dd1+"/00/wave/gridded/"+file1)
			if exists(file1)==0:
				with open('errflag.txt','w') as f:
					f.write('server error')
				exit()
				
FF="{:02}".format(fff)
wdir='/home/marcus/EACODE/cams/WAVE/'+yy1+mm1+dd1+FF

os.system("mkdir "+wdir)
os.system("mv "+file1+" "+wdir+"/")
	
for hh in [63-fff,87-fff,111-fff,135-fff,159-fff,183-fff]:
	HHH="{:03}".format(hh)
	
	print(FF,HHH)
	file1="gfswave.t"+FF+"z.global.0p16.f"+HHH+".grib2"
	print(file1)
	os.system("wget --tries=15 -T 1 https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs."+yy1+mm1+dd1+"/"+FF+"/wave/gridded/"+file1)
	os.system("mv "+file1+" "+wdir+"/")
with open('wave.pkl','wb') as f:
	pickle.dump([yy1,mm1,dd1,hh,FF],f)


