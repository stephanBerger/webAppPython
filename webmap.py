from geopy.geocoders import ArcGIS
import json
import folium
import pandas

#Wifi de marseille
dataWifi = pandas.read_csv("marseille_wifi.csv")
latWifi = list(dataWifi["LAT"])
lonWifi = list(dataWifi["LON"])
nameWifi = list(dataWifi["NOM"])


#on lit de fichier txt pour extraire 2 listes, latitude et longitude
dataFrame = pandas.read_csv("Volcanoes.txt")
lat = list(dataFrame["LAT"])
lon = list(dataFrame["LON"])
name =list(dataFrame["NAME"])
elevation = list(dataFrame["ELEV"])

data = json.load(open("service_proxy.json"))

#init objet ArcGIS()
nom = ArcGIS()

#on decode en coordonnées GPS des adresses
n = nom.geocode("avenue de marseille,Vitroles , Fr 13127")
m = nom.geocode("12 rue centrale,Fr 13013")
o = nom.geocode("1 rue de rome,Marseille,Fr 13006")
p = nom.geocode("26 rue de rome, cabries,Fr 13480")

#on cree un featureGroup pour ajouter des marker sur ce groupe , utile pour faire des layers de différents markers
fg = folium.FeatureGroup(name="Population World")

listDeCoordonnees = [o.latitude,o.longitude],[p.latitude,p.longitude]
for coordinates in listDeCoordonnees:
    fg.add_child(folium.Marker(location=coordinates, popup="Salut, je suis un marker de la map", icon=folium.Icon(color='purple')))

map = folium.Map(location=[n.latitude,n.longitude],zoom_start=12)#option ,tiles="Stamen Terrain"
fg.add_child(folium.Marker(location=[n.latitude,n.longitude], popup="C'est un marker de la carte", icon=folium.Icon(color='green')))
fg.add_child(folium.Marker(location=[m.latitude,m.longitude], popup="C'est un autre marker de la carte", icon=folium.Icon(color='red')))

def color_product(el):
    if el > 2000:
        return 'yellow'
    elif 1500 <= el <= 2000:
        return 'orange'
    elif el < 1500:
        return 'blue'
    
volcanGroup = folium.FeatureGroup(name="Volcan")
#on ajoute des markers de volcan à partir des 2 listes lat et lon , leur nom et  on revoit l'elevation dans une fonction pour avoir la couleur en fonction de l'altitude
for lt,ln,name,el in zip(lat,lon,name,elevation):
    #fg.add_child(folium.Marker(location=[lt,ln], popup=name, icon=folium.Icon(color=color_product(el))))
    volcanGroup.add_child(folium.CircleMarker(location=[lt,ln], radius=6, popup=name, fill_color=color_product(el),color='grey', fill_opacity=0.7))

wifiGroup = folium.FeatureGroup(name="Wifi Marseille")
#ajout des bornes wifi de marseille
for lt,ln,name in zip(latWifi,lonWifi,nameWifi):
    wifiGroup.add_child(folium.Marker(location=[lt,ln], popup=name, icon=folium.Icon(color=color_product(el))))

parkingGRoup = folium.FeatureGroup(name="Parking")
parkingGRoup.add_child(folium.GeoJson("service_proxy.json"))

fg.add_child(folium.GeoJson(data=open('world.json','r', encoding='utf-8-sig').read(),
                            style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 2000000 
                                                      else 'blue' if 2000000 <= x['properties']['POP2005'] <5000000 
                                                      else 'yellow' if 5000000 <= x['properties']['POP2005'] <10000000
                                                      else 'orange' if 10000000 <= x['properties']['POP2005'] <20000000
                                                      else 'red'}))
    

map.add_child(fg)
map.add_child(wifiGroup)
map.add_child(parkingGRoup)
map.add_child(volcanGroup)

map.add_child(folium.LayerControl())

map.save("index.html")