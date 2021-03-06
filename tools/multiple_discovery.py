#!/usr/bin/env python3

# Trajectory

from __future__ import print_function

import odrive.core
import time
import math
from openpyxl import load_workbook
from openpyxl import Workbook
import csv

#################### ODrive discovery ##########################################
print("\nFinding ODrives...")

ODriveSet = []

for drive in odrive.core.find_all(consider_usb=True, consider_serial=False):
    print("ODrive found, serial number: {}".format(drive.serial_number))
    ODriveSet.append(drive)

if len(ODriveSet) == 0:
    print("No ODrives found!")
    exit()
else:
    print("Found {} ODrives".format(len(ODriveSet)))

#################### PID tuning ################################################
for drive in ODriveSet:
    # M0
    drive.motor0.config.pos_gain = 5.0             # [(counts/s) / counts]
    drive.motor0.config.vel_gain = 3.0 / 10000.0   # [A/(counts/s)]
    drive.motor0.config.vel_integrator_gain = 10.0 / 10000.0
    # M1
    drive.motor1.config.pos_gain = 5.0            # [(counts/s) / counts]
    drive.motor1.config.vel_gain = 3.0 / 10000.0   # [A/(counts/s)]
    drive.motor1.config.vel_integrator_gain = 10.0 / 10000.0

#################### assign ODrives ############################################
for drive in ODriveSet:
    if drive.serial_number == 53232789697077:
        hiproll_drive      = drive
        print("Found hip roll, M0: {}, M1: {}".format(drive.motor0.error, drive.motor1.error))
    if drive.serial_number == 61977222983735:
        right_hip_drive    = drive
        print("Found left leg, M0: {}, M1: {}".format(drive.motor0.error, drive.motor1.error))
    if drive.serial_number == 61977223245879:
        left_hip_drive     = drive
        print("Found right leg, M0: {}, M1: {}".format(drive.motor0.error, drive.motor1.error))
    if drive.serial_number == 61908504096823:
        ankle_drive        = drive
        print("Found ankle pitch, M0: {}, M1: {}".format(drive.motor0.error, drive.motor1.error))