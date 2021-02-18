#!/usr/bin/env python
import rospy
from oblig2.msg import *
values=[0,0,0,0,0] #Det er ca. 6-7 punkt mellom hver lokale topp.
highestvalue=0.0 #hoyeste verdi i values
count = 0 # antall lokale topper
timeinmillis = float(0)

def print_values(data):
    print("filtered data:" + str(data.filtered) + " raw data: " + str(data.raw))
    global highestvalue
    global count
    global values
    global timeinmillis
    highestvalue = max(values)
    values.append(data.filtered)
    values.pop(0) #fjerner eldste verdi fra values, slik at vi aldri sammenligner 2 topper med hverandre
    if highestvalue < data.filtered and highestvalue != 0:
        count+=1
    timeinmillis+=142.8571428571  #oppdateringsfrekvensen er pa 7hz
    print (count/(timeinmillis/1000))*60 #regner ut og printer puls

def evaluate_data():
    rospy.init_node('evaluate_data', anonymous=True)

    rospy.Subscriber("fpmg_filtered", filtered_value, print_values)

    rospy.spin()

if __name__ == '__main__':
    rospy.wait_for_service('do_filter_calc')
    evaluate_data()