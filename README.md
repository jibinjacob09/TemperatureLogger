# TemperatureLogger

## Motivation

I wanted to build my own temperature logging system using Raspbery PI and some cheap temperature sensors (DS18B20).

I wanted to store the temperature data in a time series format, which then can potentially be used by a graph UI like
Graphana.  

This repo contains the code that I used to read data from the sensors, and write to my instance of InfluxDB.


## How everything should work in big picture

There are 3 main software components to this system (listed below), and each of them will be run in its own
 docker container

1. Grafana, [more info](https://grafana.com/docs/installation/docker/)
1. InfluxDB, [more info](https://docs.docker.com/samples/library/influxdb/)
1. For this python code

Note: I didnt use a docker-compose.yaml, since it proved to unreliable on a PI

## How to run this code

1. create a `sensors_info` file by following the `sensors_info.example` file with all sensors info.
1. Run the InfluxDB container and choose an appropriate volume to store data

    ```docker run -p 8086:8086 -v ~/.influxdb:/var/lib/influxdb --restart=always influxdb```
1. Run the Grafana container

    ```docker run -d -p 3000:3000 --restart=always grafana/grafana```
1. Build the python code's image using dockerfile
    
    i. Replace the `localhost` reference in main.py (and test_main.py) with the actual ip of your device
    
    ```docker build . -t  templogger_python```

1. Run the templogger_python image as a container .

    i. set `$sensors_data` with the location of the folder that contains all sensors output data.  
    In Raspberry Pi it is  `/sys/devices/w1_bus_master1/`
    
    ```docker run -d -v ${sensors_data}:/w1_bus_master1 --restart=always templogger_python```

1. Go to `localhost:3000` (or whichever port you used for Grafana) to login and create your dashboard

## Running Tests

All tests are located in `tests/` directory, and will need pytest to run

``` pytest test/```  

note:  test_main will require a running influxdb container. Update the ip and port as needed
