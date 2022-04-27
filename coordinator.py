import subprocess
import time
import gpxpy
import gpxpy.gpx
import numpy as np
from random import randint

ROUTE = "./data/smallroute.gpx"
class Docker:
    def get_containers():
        return subprocess.check_output("sudo docker ps -q".split()).decode("utf-8").splitlines()

class Phone:
    def __init__(self, container):
        self.container = container
        self.prefix = "sudo docker exec -it {}".format(self.container)
    def initialize(self):
        subprocess.run("{} adb shell am start -a android.intent.action.MAIN -n com.google.android.apps.maps/com.google.android.maps.MapsActivity".format(self.prefix).split())
        subprocess.run("{} adb shell pm grant com.google.android.apps.maps android.permission.ACCESS_COARSE_LOCATION".format(self.prefix).split())
        subprocess.run("{} adb shell pm grant com.google.android.apps.maps android.permission.ACCESS_FINE_LOCATION".format(self.prefix).split())
        subprocess.run("{} adb shell settings put secure location_providers allowed +gps".format(self.prefix).split())
        subprocess.run("{} adb shell settings put secure location_providers allowed +network".format(self.prefix).split())
        subprocess.run("{} adb shell settings put secure location_mode 3".format(self.prefix).split())

    def move(self, coord):
        subprocess.run("{} adb emu geo fix {} {}".format(self.prefix, str(coord[0]), str(coord[1])).split())


def interpolate(l, times):
    new = []
    for i in range(len(l)-2):
        if (l[i+1]-l[i]) == 0:
            new.extend([l[i]]*times)
        else:
            new.extend(list(np.arange(l[i],l[i+1], (l[i+1]-l[i])/times)))
    new.append(l[len(l)-1])
    return new


if __name__ == "__main__":
    gpx_file = open(ROUTE, "r")
    gpx = gpxpy.parse(gpx_file)

    phones = list(map(lambda cid: Phone(cid), Docker.get_containers()))
    
    for i, phone in enumerate(phones):
        phone.initialize()
    
    lats = []
    longs = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lats.append(point.latitude)
                longs.append(point.longitude)
    lats_interp = interpolate(lats, 3)
    longs_interp = interpolate(longs, 3)

    for point,_ in enumerate(lats_interp):
        for i,phone in enumerate(phones):
            location = (longs_interp[i*2+point], lats_interp[i*2+point])
            phone.move(location)
        
        if point > 10 and randint(0,1) > 0.5:
            print("sleeping")
            time.sleep(randint(0,60))
            

