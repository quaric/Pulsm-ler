#!/usr/bin/env python
from __future__ import print_function
from oblig2.msg import raw_sensor_value
from oblig2.srv import filtered_sensor_value,filtered_sensor_valueResponse
import rospy

uqueue = [0,0] #holder pa raw voltage fra siste 3 
yqueue = [0,0] #holder pa y-filterverdi fra siste 3
#koeffisienter fra matlab
a1 = 0.3589
a2 = 0.0677
b1 = 1.0707
b2 = 0.3559
def handle_raw_sensor_value(raw):
    uqueue.append(raw.voltage)
    u1 = uqueue.pop(0)
    u2 = uqueue[0]
    y1 = yqueue.pop(0)
    y2 = yqueue[0]
    y = -a1*y1 - a2*y2 + b1*u1 + b2*u2 #formel for utregning av filterverdi
    yqueue.append(y)
    print(y)
    return filtered_sensor_valueResponse(y, raw.voltage)
def do_filter_calc():
    rospy.init_node('do_filter_calc_service')
    s = rospy.Service('do_filter_calc', filtered_sensor_value,handle_raw_sensor_value)
    print("Ready to filter")
    rospy.spin()

if __name__ == "__main__":
    do_filter_calc()