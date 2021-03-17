# -*- coding: UTF-8 -*-


"""
# advanced options of lib init
# from __future__ import print_function
# blynk = blynklib.Blynk(BLYNK_AUTH, server='blynk-cloud.com', port=80, ssl_cert=None,
#                        heartbeat=10, rcv_buffer=1024, log=print)

# Lib init with SSL socket connection
# blynk = blynklib.Blynk(BLYNK_AUTH, port=443, ssl_cert='<path to local blynk server certificate>')
# current blynk-cloud.com certificate stored in project as 
# https://github.com/blynkkk/lib-python/blob/master/certificate/blynk-cloud.com.crt
# Note! ssl feature supported only by cPython

# register handler for Virtual Pin V22 reading by Blynk App.
# when a widget in Blynk App asks Virtual Pin data from server within given configurable interval (1,2,5,10 sec etc) 
# server automatically sends notification about read virtual pin event to hardware
# this notification captured by current handler
"""
import time

import blynklib
import RPi.GPIO as GPIO

from controller import Controller

BLYNK_AUTH = '5EinGm43Rd0V8LeDurqn1TZyKY4DH1e-'
READ_PRINT_MSG = "[READ_VIRTUAL_PIN_EVENT] Pin: V{}"
WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
# base lib init
blynk = blynklib.Blynk(BLYNK_AUTH, log=print)

some_list = []
control_list = []


# register handler for virtual pin V2 write event
@blynk.handle_event('write V2')
def write_virtual_pin_handler(pin, values):
    some_list.append(values[0])
    # print("Write: ", WRITE_EVENT_PRINT_MSG.format(pin, value))
    # Controller(pin="V2", x_coord=value[0], y_coord=value[1])


@blynk.handle_event('write V3')
def write_virtual_pin_handler(pin, value):
    swap_direction = False
    some_list.append(value[0])
    value2 = some_list.pop()
    value1 = some_list.pop()

    control_list.append(value2)
    if int(control_list[-1]) < 127 < int(control_list[-2]):
        value2 = '127'
        value1 = '127'
        swap_direction = True
        print("Swap direction")
    elif int(control_list[-2]) < 127 < int(control_list[-1]):
        value2 = '127'
        value1 = '127'
        swap_direction = True
        print("Swap direction")
    else:
        swap_direction = False

    if len(control_list) >= 2:
        control_list.pop(0)

    print("Write: ", WRITE_EVENT_PRINT_MSG.format(pin, [value1, value2]))
    if not swap_direction:
        Controller(pin="V3", x_coord=int(value1), y_coord=int(value2))
    else:
        Controller(pin="V3", x_coord=int(value1), y_coord=int(value2))
        time.sleep(0.5)
    some_list.clear()


####################
#   LED control
####################


@blynk.handle_event('write V1')
def write_virtual_pin_handler(pin, value):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # GPIO.BOARD

    GPIO.setup(18, GPIO.OUT)  # , initial=GPIO.LOW)
    GPIO.setup(23, GPIO.OUT)  # , initial=GPIO.LOW)

    if value[0] == '1':
        GPIO.output(18, GPIO.HIGH)
        GPIO.output(23, GPIO.HIGH)

    else:
        GPIO.output(18, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)

    # GPIO.cleanup()


#
#############################################################
# main loop that starts program and handles registered events
#############################################################
while True:
    blynk.run()
