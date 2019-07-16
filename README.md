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


## How to run this code

1. create a `sensors_info` file by following the `sensors_info.example` file with all sensors info.


### Notes:

This project is still WIP.  I will be making updates to it, so its possible that some things are still broken.
And yes, more documentation needs to be added.

