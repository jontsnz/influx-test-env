"""Sensor Random Data Generator
"""

import os
import sys
import argparse
import yaml
import random
import time
from datetime import datetime

class Station:
    def __init__(self, station_config):
        self.station_name = station_config['station_name']
        self.sensors = []
        for sensor_config in station_config['sensors']:
            self.sensors.append(Sensor(sensor_config))

class Sensor:
    def __init__(self, sensor_config):
        self.name = list(sensor_config.keys())[0]
        self._min = sensor_config[self.name]['min']
        self._max = sensor_config[self.name]['max']
        self.reading = sensor_config[self.name]['start']
        self._last_direction = 1
        self._dp = sensor_config[self.name]['dp']
        self._max_step = sensor_config[self.name]['max_step']

    def generate_reading(self):
        step = self._max_step * random.random()
        if random.random() < 0.9:
            direction = self._last_direction
        else:
            direction = -1 * self._last_direction
        if (self.reading + (step * direction) > self._max) or (self.reading + (step * direction) < self._min):
            direction = -1 * direction
        reading = round(self.reading + (step * direction),self._dp)
        self.reading = reading
        self._last_direction = direction
        return reading

def generate_readings(config):
    station = Station(config['station'])
    max_iterations = config['settings']['iterations']
    print('Generating %d readings for station: %s' % (max_iterations, station.station_name))
    cnt = 0
    while (cnt < max_iterations) or (max_iterations == -1):
        cnt += 1
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        readings = [('TIMESTAMP', timestamp),('RECORD', cnt),('Station', station.station_name)]
        readings.extend([(s.name, s.generate_reading()) for s in station.sensors])
        print(readings)
        time.sleep(config['settings']['interval_secs'])

def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-c', '--configfile', help="Config file")
    args = parser.parse_args(arguments)

    with open(args.configfile) as config_file:
        try:
            config = yaml.safe_load(config_file)
        except yaml.YAMLError as exc:
            print(exc)

    if config:
        generate_readings(config)
    else:
        print('Config file must be provided')

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
