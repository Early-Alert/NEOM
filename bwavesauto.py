#### import modules

import matplotlib.pyplot as plt
import geopandas 
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy
from cartopy.util import add_cyclic_point
import pygrib
import os
import imageio
from geopy import distance
from shapely.geometry import Point, Polygon
from scipy import interpolate 
from scipy.ndimage import gaussian_filter
import pickle
import glob
from osgeo import gdal
from osgeo import gdal_array
from osgeo import osr,ogr

with open("wave.pkl",'rb') as f:
	wavep=pickle.load(f)
# specify timeframe
year1=wavep[0]
year2=wavep[0]
#year2="2023"
month1=wavep[1]
month2=wavep[1]
#month2="02"
#day1="22"
day1=wavep[2]
day2=wavep[2]
hour1=wavep[3]
hour2=wavep[3]
#hour1=39
#hour2=39
latmax=50
latmin=10
lonmmax=60
lonmmin=10
lonmin=-115
lonmax=-85
hrun=wavep[4]
varms=[1]

# directories and file_lists for GFS data

gfsdir='/home/marcus/EACODE/cams/WAVE/'+year1+month1+day1+hrun
#wrfdir='/run/media/marcus/Expansion/CAMScams/WRFCOMP/'+year1+month1+day1+'00'
#mrmsdir='../cams/MRMS/'+year1+month1+day1+'00'

# create string array of hours from integer range of hours
hours=["{:02}".format(n) for n in range(hour1,hour2+1,6)]
# another way (e.g.):  [str(i).zfill(2) for i in range(hour1,hour2+1)]

#construct list of grib files for fv3 and wrf

#format e.g.:  2022112900/fv3NSSL_2022112900f035.grib2
gfs_files=glob.glob(gfsdir+'/gfswave*')
#print(gfs_files,'b4sort')

#gfs_files.sort(key=lambda x:x.split('.')[4])
#print(gfs_files,'aftersort')
snowall=[]
print(gfsdir)
print(gfs_files)
print(hours)
for i,gfsfile in enumerate(gfs_files):
	ref=[]
	grb=pygrib.open(gfsfile)
	
	for j,varm in enumerate(varms): # 2 vars
		gmsg=(grb.message(varm))
		ref.append(gmsg.values)
		
	print(i,len(ref),ref[0].shape,gfsfile)	

#gfs lons are 0-360
	lats,lons=gmsg.latlons()

	where=np.where((lats < latmax)&(lats > latmin)&(lons < lonmmax)&(lons > lonmmin))
	boxx=where[0]
	boxy=where[1]
	x1=np.min(boxx)
	x2=np.max(boxx)
	y1=np.min(boxy)
	y2=np.max(boxy)
	latc=lats[x1:x2,y1:y2]
	lonc=lons[x1:x2,y1:y2]

#	grab 'box' of model grib data, set negative flagged data to zero

	refb0=ref[0][x1:x2,y1:y2]
	refb0[refb0<0]=0
#	refb1=ref[1][x1:x2,y1:y2]
#	refb1[refb1<0]=0
	snow=np.zeros([refb0.shape[0],refb0.shape[1]])
	print(snow.shape,snow[0,0])
	snow[refb0>=-1]=refb0[refb0>-1]
	snow[snow>=9999]=0
	print(snow.shape,snow[0,0])
	print(snow)
#	snow=refb0#*refb1*10/25
#	array=snow

### plot REFS function

	def plotrefs(refc,model,REFS,ti):
		ax=plt.axes(projection=ccrs.PlateCarree())

		cs=ax.contourf(loncc, latcc,refc,transform = ccrs.PlateCarree())

		ax.coastlines()
		ax.add_feature(cfeature.STATES.with_scale('10m'), facecolor='none', edgecolor='black')
		plt.colorbar(cs,shrink=0.5)

		plt.suptitle(model+REFS+' '+month1+day1+hrun+', f'+hours[ti]+', 12 UTC Run')
		plt.savefig(model+'-'+REFS+'_'+month1+day1+hrun+'00f'+hours[ti]+'.png',dpi=400)
		plt.close()

# call the plot REFS function 
#	plotrefs(refb0,'GFS','ACPC',i)
#	plotrefs(refb1,'GFS','CSNOW',i)
	snow[np.isnan(snow)]=0
#	snow[0,0]=0
	print('k',snow[0,0])
#	plotrefs(refb0,'WAVE','SigHeight',i)
	array=2.23694*snow.copy()
	
	print (array.max())
	array[(array < 1)]=0
	array[((array >0) & (array <3))] = 1
	array[((array > 1) & (array < 7))] = 2
	array[(array > 2) & (array < 12)] = 3
	array[(array > 3) & (array < 24)] = 4
	print (array.max(),'h')
	array[(array > 4) & ( array < 31)] = 5
	array[(array > 5) & (array < 38)] = 6
	array[(array > 6) & (array < 46)] = 7
	array[(array > 7) & ( array < 54)] = 8
	array[(array > 8) & (array < 63)] = 9
	array[(array > 9) & (array < 72)] = 10
	array[(array > 10) & (array < 83)] = 11
	array[(array > 11) & (array < 300)] = 12	
	print (array.max(),'h')
	
	
	
	
	
	lonmin=np.min(lonc)
	lonmax=np.max(lonc)
	latmin=np.min(latc)
	latmax=np.max(latc)

	
	
	
	
	dlat = 0.01           # regular step (deg) for the common lat 
	dlon = 0.01          # regular step (deg) for the common lon  - around 1 km at 60N

		# Grid dimensions		
	Nlat = int(np.abs(latmax-latmin)/dlat)+1
	Nlon = int(np.abs(lonmax-lonmin)/dlon)+1

		# Lat-Lon vector
	reg_lat = np.linspace(latmin, latmax, Nlat)  # regularly spaced latitude vector
	reg_lon = np.linspace(lonmin, lonmax, Nlon)  # regularly spaced longitude vector
		# Lat-Lon regular Grid
	reg_lon_mesh, reg_lat_mesh = np.meshgrid(reg_lon, reg_lat)

	refc = interpolate.griddata((lonc.ravel(), latc.ravel()), array.ravel(),\
		(reg_lon_mesh, reg_lat_mesh), method='linear')
	
###    *** latc, lonc are now the common latitude and longitude meshes used for plotting, etc
	loncc=reg_lon_mesh
	latcc=reg_lat_mesh
	
	
	
	array=refc.copy()
	
	array=np.flipud(array)
	array=gaussian_filter(array,5)
	array=np.round(array)
#	array=gaussian_filter(array,10)
#	array=np.round(array/25)*25
	print(np.max(array),np.min(array))
	#plotrefs(array,'WAVE','SigHeight',i)


	loncc[loncc>180]=loncc[loncc>180]-360



	xmin,ymin,xmax,ymax = [loncc.min(),latcc.min(),loncc.max(),latcc.max()]
	nrows,ncols = np.shape(array)
	xres = (xmax-xmin)/float(ncols)
	yres = (ymax-ymin)/float(nrows)
	geotransform=(xmin,xres,0,ymax,0, -yres)   
# That's (top left x, w-e pixel resolution, rotation (0 if North is up), 
#         top left y, rotation (0 if North is up), n-s pixel resolution)

	output_raster = gdal.GetDriverByName('GTiff').Create('myraster.tif',ncols, nrows, 1 ,gdal.GDT_Float32)  # Open the file
	output_raster.SetGeoTransform(geotransform)  # Specify its coordinates
	srs = osr.SpatialReference()                 # Establish its coordinate encoding
	srs.ImportFromEPSG(4326)                     # This one specifies WGS84 lat long.

	output_raster.SetProjection( srs.ExportToWkt() )   # Exports the coordinate system 
                                                                            # to the file
                                                   
                                                   
	output_raster.GetRasterBand(1).WriteArray(array)   # Writes my array to the raster
	output_raster.GetRasterBand(1).SetNoDataValue(0)
	srcband=output_raster.GetRasterBand(1)


	drv = ogr.GetDriverByName("ESRI Shapefile")
	dst_ds = drv.CreateDataSource("testout.shp")

	dst_layer = dst_ds.CreateLayer("testgis", srs  )
	fld = ogr.FieldDefn("risk", ogr.OFTInteger)
	dst_layer.CreateField(fld)
	dst_field = dst_layer.GetLayerDefn().GetFieldIndex("risk")

	gdal.Polygonize( srcband, None, dst_layer, dst_field, [], callback=None )


	output_raster.FlushCache()
	del dst_ds


	shp_file = geopandas.read_file('testout.shp')
	print(shp_file[shp_file['risk']>0])
	shp_file=shp_file[shp_file['risk']>0]
	shp_file.to_file('Beaufort'+str(i+1)+'.geojson', driver='GeoJSON')	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
params=[year1,year2,month1,month2,day1,day2,hour1,hour2,hours,latc,lonc,snowall]
with open('WAVE-TEST_'+year1+month1+day1+hrun+"f0"+str(hour1)+'-'+str(hour2)+'.pkl','wb') as rf:
	pickle.dump(params,rf,pickle.HIGHEST_PROTOCOL)

