# Traffic Jam spoofer for GMaps

Give it a Google Maps Route (https://mapstogpx.com/) and see if you can spoof a traffic jam.
Its an untested hypothesis and so far it didn't work locally. However, maybe it works when distributing the docker containers over multiple AWS EC2 instances (or other cloud providers).

# Requirements
- Python 3
- Docker

# How it works?

The idea is somewhat based on the Nagel–Schreckenberg model

- Emulate a bunch of android phones
- Start Google Maps and set needed permissions
- Enable GPS Tracking
- Read in a route and set the GPS coordinates according to the route
- slowly move towards the target, potentially interpolating the route with a sleeping probability

# How to run?
- Configure the route in coordinator.py
- Start the phones
```
docker-compose up -d
``` 
- Run the coordination script to let the devices move
```
python3 coordinator.py
```

