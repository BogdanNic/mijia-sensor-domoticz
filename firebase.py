import requestsimport datetimeimport timefrom mijia.mijia_poller import MijiaPoller, \    MI_HUMIDITY, MI_TEMPERATURE, MI_BATTERYimport firebase_domaind = datetime.datetime.now()currentDate = int(d.timestamp() * 1000)url = firebase_domain.my_domaindef firebase_request(url, temperature, humidity, comfort, battery):    # The old way is need here    myobj = '{"temperature": %s, "humidity" : %s, "comfort" : %s, "battery": %s}' % (    temperature, humidity, comfort, battery)    # myobj = f"{'temperature': {temperature}}"    request = requests.put(url + "/{}.json".format(currentDate), data=myobj)    print(request.text)    return request.textdef update(address, idx_temp):    poller = MijiaPoller(address)    loop = 0    try:        temp = poller.parameter_value(MI_TEMPERATURE)    except:        temp = "Not set"    while loop < 2 and temp == "Not set":        print("Error reading value retry after 5 seconds...\n")        time.sleep(5)        poller = MijiaPoller(address)        loop += 1        try:            temp = poller.parameter_value(MI_TEMPERATURE)        except:            temp = "Not set"    if temp == "Not set":        print("Error reading value\n")        return    print("Mi Sensor: " + address)    print("Firmware: {}".format(poller.firmware_version()))    print("Name: {}".format(poller.name()))    print("Temperature: {}°C".format(poller.parameter_value(MI_TEMPERATURE)))    print("Humidity: {}%".format(poller.parameter_value(MI_HUMIDITY)))    print("Battery: {}%".format(poller.parameter_value(MI_BATTERY)))    val_bat = "{}".format(poller.parameter_value(MI_BATTERY))    # Update temp    # val_temp = "{}".format(poller.parameter_value(MI_TEMPERATURE))    # domoticzrequest("http://" + domoticzserver + "/json.htm?type=command&param=udevice&idx=" + idx_temp + "&nvalue=0&svalue=" + val_temp + "&battery=" + val_bat)    # Update humidity    # val_hum = "{}".format(poller.parameter_value(MI_HUMIDITY))    # domoticzrequest("http://" + domoticzserver + "/json.htm?type=command&param=udevice&idx=" + idx_hum + "&svalue=" + val_hum + "&battery=" + val_bat)    # /json.htm?type=command&param=udevice&idx=IDX&nvalue=0&svalue=TEMP;HUM;HUM_STAT    val_temp = "{}".format(poller.parameter_value(MI_TEMPERATURE))    val_hum = "{}".format(poller.parameter_value(MI_HUMIDITY))    val_comfort = "0"    if float(val_hum) < 40:        val_comfort = "2"    elif float(val_hum) <= 70:        val_comfort = "1"    elif float(val_hum) > 70:        val_comfort = "3"    response = firebase_request(url, val_temp, val_hum, val_comfort, val_bat)    print(response)# response = firebase_request(url, 2, 2, 2, 2)# response = firebase_request(url, val_temp, val_hum, val_comfort, val_bat)update("58:2D:34:34:3D:AF", "723")