#!/usr/bin/env python
import rospy
from oblig2.msg import raw_sensor_value
import Adafruit_BBIO.ADC as ADC
import time
import threading
import Queue

# Analog sensor til input fra TCRT1000
sensor = "P9_40"
# Filvei til DS18B20P temperatur sensor "fil"
w1 = "/sys/bus/w1/devices/28-00000b347c50/w1_slave"

ADC.setup()

q = Queue.Queue() #bruker queue for aa kommunisere mellom traader, slik at vi faar hentet temperaturverdien
# Maa kjores pa annen traad da ds18b20 har en 750-800ms svartid.
def checkTemperature():
    while True:
        raw_temp = open(w1, "r").read()
        formatted_temp = float(raw_temp.split("t=")[-1]) / 1000  # formatterer
        q.put_nowait(formatted_temp)


t = threading.Thread(target=checkTemperature)
t.daemon = True  # so traaden stopper pa interrupt
t.start()
time.sleep(0.8) #venter 800ms saa vi far hentet forste temperaturverdi foer vi begynner aa sjekke trct1000
temp = float()

#hovedmetode som henter oppretter noden som publisher paa fpmg_raw og sjekker sensorverdier, som publiseres
def fotoplesmytograf():
    pub = rospy.Publisher('fpmg_raw', raw_sensor_value, queue_size=10)
    rospy.init_node('fotoplesmytograf', anonymous=True)
    rate = rospy.Rate(7)
    time=float(0.0)
    while not rospy.is_shutdown():
        if not q.empty():
            temp = q.get_nowait()
        msg = raw_sensor_value(time,ADC.read(sensor),temp)
        rospy.loginfo(msg)
        pub.publish(msg)
        time+=142.8571428571
        rate.sleep()

if __name__ == '__main__':
    try:
        fotoplesmytograf()
    except rospy.ROSInterruptException:
        pass
