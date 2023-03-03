import json 
from arcgis.gis import GIS 
from arcgis.features import FeatureSet

def empty_layer(layer,where_str="1=1"):
    list_of_ids = [f.get_value(layer.properties.objectIdField) for f in layer.query(where=where_str).features]
    if(len(list_of_ids) > 0):
        layer.edit_features(deletes=list_of_ids)



portal_url = "https://maps.earlyalert.com/portal"
portal_user = "EA_Developer4"###
portal_password = "zxcVBN77**"
gis = GIS(portal_url, portal_user, portal_password)

#print(gis)

#id 781d65971ee64e329eb0314fbdc7a5fb

##CLEAR THE LAYER BEFORE ADDING NEW RECORDS
def empty_layer(layer,where_str="1=1"):
    list_of_ids = [f.get_value(layer.properties.objectIdField) for f in layer.query(where=where_str).features]
    if(len(list_of_ids) > 0):
        results=layer.edit_features(deletes=list_of_ids)
        print(results)
      
id=["c1e9dae713924c23858826d34ce9f3cc",
"c19f5e078c9042788c7a949f908df135",
"ec7761aa5f1a44268b5a074ff158af84",
"eb6d0717739a41f8a4d4806d59ecc096",
"cbf0408bc49448d2a0f10e066eff3dc0",
"db1f0cf25bdc4ef7a590863a2e932811",
"e6299b55c75b44ee8b62dbb46dfca0e6",
"328846a5e5014e90af2b49533a2f955d",
"047819c9265145f1805ca40a68b9827f",
"971b1d7b00d2466286340bc5a79f39cd"]
      
      
        
for i,file in enumerate(["gfswaveday1.geojson","gfswaveday2.geojson","gfswaveday3.geojson",
"gfswaveday4.geojson","gfswaveday5.geojson","gfswaveday6.geojson","gfswaveday7.geojson","Beaufort1.geojson",
"Beaufort2.geojson","Beaufort3.geojson"]):
	with open(file) as f:        
    # returns JSON object as 
    # a dictionary
   	 geojson = json.load(f)
   


#
	fs=FeatureSet.from_geojson(geojson)
#next(filter(lambda x:x['name'] == 'risk',fs.fields),None)["type"]='esriFieldTypeInteger'
#next(filter(lambda x:x['name'] == 'risk',fs._fields),None)["type"]='esriFieldTypeInteger'




	risk_layer=gis.content.get(id[i])
	flayer = risk_layer.layers[0]
	empty_layer(flayer)

	results=flayer.edit_features(adds=fs.features)

	print("DONE -- {}".format(len(results['addResults'])))
