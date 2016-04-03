from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests
import math
app = Flask(__name__)
client = MongoClient()
db = client.subway

cursor = db.stations.find_one({"type":"FeatureCollection"})

def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x2-x1,2) + math.pow(y2-y1,2))

@app.route("/getNearestTrainStation")
def getNearestTrainStation():
    """
    Gets the nearest train station to a given point.
    args:
        point: the longitude/latitude point to locate around.
    returns:
        data for the nearest train station in json format.
    """
    point = request.args.get("point")
    points = point.split(",")
    longitude = float(points[0][1:])
    latitude = float(points[1][:len(points[1])-1])
    minimum = 1000000
    closest = None
    for station in cursor.get("features"):
        coords = station.get("geometry").get("coordinates")
        if distance(longitude, latitude, coords[0], coords[1]) < minimum:
            minimum = distance(longitude, latitude, coords[0], coords[1])
            closest = station
    minimum=1000000
    return jsonify(closest)




@app.route("/getNearestTrainStationByLine")
def getNearestTrainStationByLine():
    """
    Gets the nearest train station to a given point based on subway lines.
    args: 
        point: the longitude/latitude point to locate around.
        line: subway line to filter by.
    returns:
        data for the train station in json format.
    """
    pass

@app.route("/getNearestXTrainStations")
def getNearestXTrainStations():
    """
    Gets the nearest X train stations to a given point based on subway lines.
    args:
        point: the longitude/latitude point to locate around.
        number: the number of train stations to return.
    returns:
        data for the train stations in json format.
    """
    pass



if __name__ == '__main__':
    app.debug=True
    app.run("localhost", port=8000)