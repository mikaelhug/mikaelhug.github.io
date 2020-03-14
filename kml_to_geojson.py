from os import listdir
from zipfile import ZipFile
import json
import os
import shutil
from shutil import copyfile

nc_path = '/home/mikael/Nextcloud/Route/'
kml_path = '/home/mikael/mikaelhug.github.io/kml_files/'
data_path = '/home/mikael/mikaelhug.github.io/data.json'
kml_files = listdir(nc_path)

with open(data_path, 'r') as f:
    data = json.load(f)

already_added_routes = []
for route in data['features']:
    already_added_routes.append(route['properties']['tag'])


def s_turn(kmldata, splitter):
    try:
        return kmldata.split(splitter)[1].split('</value>')[0].split('<value>')[1]
    except:
        return 0


def all_kmz_to_kml():
    kml_files_git = listdir(kml_path)
    for kml in kml_files:
        kmlname = kml.split('.')[0]+'.kml'

        # pass if already copied
        if kmlname in kml_files_git:
            print("KML already exists: "+kmlname)
            continue

        # copy .kmz from nextcloud to git
        copyfile(nc_path+kml, kml_path+kml)

        # extract kmz to 'temp'
        os.mkdir(kml_path+'temp')
        zip = ZipFile(kml_path+kml)
        zip.extractall(kml_path+'temp')

        # move kml to ../
        shutil.move(kml_path+'temp/doc.kml', kml_path+kmlname)

        # delete 'temp' + kmz in git
        shutil.rmtree(kml_path+'temp')
        os.remove(kml_path+kml)

        print("Copied: "+kmlname)


def kml_to_geo():
    kml_files_git = listdir(kml_path)

    for kml in kml_files_git:
        if kml in already_added_routes:
            print("Route already exists: "+kml)
            continue

        with open(kml_path+kml, 'r') as f:
            kmldata = f.read()

        name = kmldata.split('<name>')[1].split('</name>')[0]
        day = "monday"
        description = kmldata.split('<description>')[1].split('</description>')[0]
        tag = kml
        distanceTotal = s_turn(kmldata, 'distanceTotal')
        timeMoving = s_turn(kmldata, 'timeMoving')
        maxSpeed = s_turn(kmldata, 'maxSpeed')
        createdDate = s_turn(kmldata, 'createdDate')
        endDate = s_turn(kmldata, 'endDate')
        distanceTotalUp = s_turn(kmldata, 'distanceTotalUp')
        distanceTotalDown = s_turn(kmldata, 'distanceTotalDown')
        timeMovingDown = s_turn(kmldata, 'timeMovingDown')
        timeMovingUp = s_turn(kmldata, 'timeMovingUp')
        downTotal = s_turn(kmldata, 'downTotal')
        upTotal = s_turn(kmldata, 'upTotal')
        averageKmPace = s_turn(kmldata, 'averageKmPace')
        lastKmPace = s_turn(kmldata, 'lastKmPace')
        maxKmPace = s_turn(kmldata, 'maxKmPace')

        coords = []
        coordsdata = kmldata.split('<LineString>')[1].split('</LineString>')[0]
        coordsdata = coordsdata.split('<coordinates>')[1].split('</coordinates>')[0]
        coordsdata = coordsdata.split()

        for c in coordsdata:
            c = c.split(',')
            lat = c[0]
            lang = c[1]
            alt = c[2]
            
            coord = [lat,lang,alt]
            coords.append(coord)

        dict_add = {
            "type": "Feature",
            "properties": {
                "name": name,
                "day": day,
                "description": description,
                "tag": tag,
                "distanceTotal": distanceTotal,
                "timeMoving": timeMoving,
                "maxSpeed": maxSpeed,
                "createdDate": createdDate,
                "endDate": endDate,
                "distanceTotalUp": distanceTotalUp,
                "distanceTotalDown": distanceTotalDown,
                "timeMovingDown": timeMovingDown,
                "timeMovingUp": timeMovingUp,
                "downTotal": downTotal,
                "upTotal": upTotal,
                "averageKmPace": averageKmPace,
                "lastKmPace": lastKmPace,
                "maxKmPace": maxKmPace

            },
            "geometry": {
                "type": "LineString",
                "coordinates": coords
            }
        }

        data['features'].append(dict_add)

    with open(data_path, 'w') as f:
        json.dump(data, f)


all_kmz_to_kml()
print("\n")
kml_to_geo()