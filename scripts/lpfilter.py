#!/usr/bin/env python
import rospy
from oblig2.msg import *
from oblig2.srv import *
#sender filter_raw_values.srv til do_filter_calc nar den mottar verdier for fotoplesmytograf.py 
def filter_values(data):
    try:
        filter_raw_values = rospy.ServiceProxy('do_filter_calc', filtered_sensor_value)
        response = filter_raw_values(data.timeinmillis, data.voltage, data.temperature)
        handle_filtered_values(response)
    except rospy.ServiceException as e:
        print("Service called failed: " + e)

#publiserer til fpmg_filtered
def handle_filtered_values(data):
    msg = filtered_value(data.sum, data.raw)
    if not rospy.is_shutdown():
        rospy.loginfo(msg)
        pub.publish(msg)

def lpfilter():
    rospy.init_node('lpfilter', anonymous=True)

    rospy.Subscriber("fpmg_raw", raw_sensor_value, filter_values) #subscriber til fpmg_raw 
    global pub #slik jeg kan bruke den i handle_filtered_values metoden
    pub = rospy.Publisher('fpmg_filtered', filtered_value, queue_size=10) #publiserer til fpmg_filtered

    rospy.spin()

if __name__ == '__main__':
    rospy.wait_for_service('do_filter_calc')
    lpfilter()
