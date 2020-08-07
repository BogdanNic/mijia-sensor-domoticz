# -*- coding: utf-8 -*-

import time
import datetime
import requests
import firebase_domain
from mijia.mijia_poller import MijiaPoller, \
    MI_HUMIDITY, MI_TEMPERATURE, MI_BATTERY


def firebase_request(url, temperature, humidity, comfort, battery):
    # d = datetime.datetime.now()
    # current_date = int(d.timestamp() * 1000)
    # The old way is need here
    myobj = '{"date":{".sv":"timestamp"},"temperature": %s, "humidity" : %s, "comfort" : %s, "battery": %s}' % (temperature, humidity, comfort, battery)
    # myobj = f"{'temperature': {temperature}}"
    request = requests.post(url + ".json", data=myobj)
    print("Response is ".format(request.text))
    return request.text


def update(address, idx_temp):
    poller = MijiaPoller(address)
    loop = 0
    try:
        temp = poller.parameter_value(MI_TEMPERATURE)
    except:
        temp = "Not set"

    while loop < 2 and temp == "Not set":
        print("Error reading value retry after 5 seconds...\n")
        time.sleep(5)
        poller = MijiaPoller(address)
        loop += 1
        try:
            temp = poller.parameter_value(MI_TEMPERATURE)
        except:
            temp = "Not set"

    if temp == "Not set":
        print("Error reading value\n")
        return

    print("Mi Sensor: " + address)
    print("Firmware: {}".format(poller.firmware_version()))
    print("Name: {}".format(poller.name()))
    print("Temperature: {}°C".format(poller.parameter_value(MI_TEMPERATURE)))
    print("Humidity: {}%".format(poller.parameter_value(MI_HUMIDITY)))
    print("Battery: {}%".format(poller.parameter_value(MI_BATTERY)))

    val_bat = "{}".format(poller.parameter_value(MI_BATTERY))
    val_temp = "{}".format(poller.parameter_value(MI_TEMPERATURE))
    val_hum = "{}".format(poller.parameter_value(MI_HUMIDITY))

    val_comfort = "0"
    if float(val_hum) < 40:
        val_comfort = "2"
    elif float(val_hum) <= 70:
        val_comfort = "1"
    elif float(val_hum) > 70:
        val_comfort = "3"
    url = firebase_domain.my_domain
    firebase_request(url, val_temp, val_hum, val_comfort, val_bat)


update("58:2D:34:34:3D:AF", "723")
# firebase_request(url, 10, 10, 10, 10)