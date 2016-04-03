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
        line (optional): specifies the train line
    returns:
        data for the nearest train station in json format.
    """
    point = request.args.get("point")
    line = request.args.get("line") or None
    points = point.split(",")
    longitude = float(points[0][1:])
    latitude = float(points[1][:len(points[1])-1])
    minimum = 1000000
    closest = None
    for station in cursor.get("features"):
        coords = station.get("geometry").get("coordinates")
        if distance(longitude, latitude, coords[0], coords[1]) < minimum:
            if line is not None:
                if line in station.get("properties").get("line"):
                    minimum = distance(longitude, latitude, coords[0], coords[1])
                    closest = station
            else:
                minimum = distance(longitude, latitude, coords[0], coords[1])
                closest = station

    minimum=1000000
    line = None
    j = jsonify(closest)
    closest = None
    return j



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
    point = request.args.get("point")
    number = int(request.args.get("number"))
    points = point.split(",")
    longitude = float(points[0][1:])
    latitude = float(points[1][:len(points[1])-1])
    minimum = 1000000
    closest = None

    distances = [
        distance(longitude,
            latitude,
            station.get("geometry").get("coordinates")[0],
            station.get("geometry").get("coordinates")[1]
            ) for station in cursor.get("features")
    ]



    distances.sort()
    top_n = distances[0:number]
    # # }},
    output = []
    for i in top_n:
        for station in cursor.get("features"):
            if i==distance(longitude,
            latitude,
            station.get("geometry").get("coordinates")[0],
            station.get("geometry").get("coordinates")[1]
            ):
                output.append(station)


    return jsonify({"top_" + str(number):output})
if __name__ == '__main__':
    app.debug=True
    app.run("localhost", port=8000)