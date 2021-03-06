#!/usr/bin/env python3

# Trajectory

from __future__ import print_function

import odrive.core
import time
import math
from openpyxl import load_workbook
from openpyxl import Workbook
import csv

#################### adjustable parameters #####################################
trajectory_file_path = 'traj_test.csv' # trajectory CSV file
speed_multiplier = 8                     # speed multiplier, for faster movement

print("\nRunning trajectory from {}".format(trajectory_file_path))
print("Trajectory speed multiplier: {}".format(speed_multiplier))

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
    if drive.serial_number == 61977222983735:
        right_hip_drive    = drive
    if drive.serial_number == 61977223245879:
        left_hip_drive     = drive
    if drive.serial_number == 61908504096823:#53207016616246:
        ankle_drive        = drive

offset_left_slide  = left_hip_drive.motor0.pos_setpoint
offset_left_pitch  = left_hip_drive.motor1.pos_setpoint
offset_right_slide = right_hip_drive.motor0.pos_setpoint
offset_right_pitch = right_hip_drive.motor1.pos_setpoint
offset_left_roll   = hiproll_drive.motor0.pos_setpoint
offset_right_roll  = hiproll_drive.motor1.pos_setpoint
offset_left_ankle  = ankle_drive.motor0.pos_setpoint
offset_right_ankle = ankle_drive.motor1.pos_setpoint

#################### read-in trajectory from file ##############################
right_hip_pitch_position   = []
right_hip_roll_position    = []
right_hip_slide_position   = []
right_ankle_pitch_position = []
right_ankle_roll_position  = []
left_hip_roll_position     = []
left_hip_pitch_position    = []
left_hip_slide_position    = []
left_ankle_pitch_position  = []
left_ankle_roll_position   = []

traj_size = -1

with open(trajectory_file_path) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if traj_size > -1:
            right_hip_pitch_position.append(float(row[0]))
            right_hip_roll_position.append(float(row[1]))
            right_hip_slide_position.append(float(row[2]))
            right_ankle_roll_position.append(float(row[3]))
            right_ankle_pitch_position.append(float(row[4]))
            left_hip_pitch_position.append(float(row[5]))
            left_hip_roll_position.append(float(row[6]))
            left_hip_slide_position.append(float(row[7]))
            left_ankle_roll_position.append(float(row[8]))
            left_ankle_pitch_position.append(float(row[9]))
        traj_size = traj_size + 1

print("\nTrajectory size: {}".format(traj_size))

#################### show motor error ##########################################
print("\nMotor errors")

for drive in ODriveSet:
    print("Serial_number: {}, M0: {}, M1: {}".format(drive.serial_number,
            drive.motor0.error, drive.motor1.error))

#################### zero position #############################################
print("\nReturning to zero position...")

for drive in ODriveSet:
    drive.motor0.set_pos_setpoint(0.0, 0.0, 0.0)
    drive.motor1.set_pos_setpoint(0.0, 0.0, 0.0)

#################### begin trajectory ##########################################
print("\nRunning trajectory... (press Ctrl+C to stop)")

i = 0   # counter

i_max = int(traj_size / speed_multiplier) - 100 # max value of i, calculated based
                                              #   traj size and speed multiplier

while True:
    if i > i_max:
        i = 0
        print(i)

    setpoint_index = i * speed_multiplier + 1

    setpoint_left_roll   = -45837.0 * left_hip_roll_position[setpoint_index] /2  # gear ratio: 1:36, 1/3.1415*36*4000
    setpoint_left_pitch  = 30558.0  * left_hip_pitch_position[setpoint_index] # gear ratio: 1:24, 1/3.1415*24*4000
    setpoint_left_slide  = -400000.0* left_hip_slide_position[setpoint_index] # gear ratio: 1:4, 4*4000*4, problem with encoder
    setpoint_left_ankle  = 48000.0  * left_ankle_pitch_position[setpoint_index]  # gear ratio: 1:12

    setpoint_right_roll  = -45837.0 * right_hip_roll_position[setpoint_index] /2
    setpoint_right_pitch = -30558.0 * right_hip_pitch_position[setpoint_index] # gear ratio: 1:24, 1/3.1415*24*4000
    setpoint_right_slide = 400000.0 * right_hip_slide_position[setpoint_index] # gear ratio: 1:4, 4*4000*4, problem with encoder
    setpoint_right_ankle = -48000.0 * right_ankle_pitch_position[setpoint_index] # gear ratio: 1:12

    # setpoint_right_slide = -8000 * math.sin(i/180*3.1415)+7795
    # setpoint_right_pitch = +8000 * math.sin(i/180*3.1415)+8204

    ################ sending commands to corresponding motors ##################
    left_hip_drive.motor1.set_pos_setpoint(setpoint_left_pitch+offset_left_pitch, 0.0, 0.0)
    left_hip_drive.motor0.set_pos_setpoint(setpoint_left_slide+offset_left_slide, 0.0, 0.0)
    right_hip_drive.motor1.set_pos_setpoint(setpoint_right_pitch+offset_right_slide, 0.0, 0.0)
    right_hip_drive.motor0.set_pos_setpoint(setpoint_right_slide+offset_right_slide, 0.0, 0.0)
    hiproll_drive.motor0.set_pos_setpoint(setpoint_left_roll+offset_left_roll, 0.0, 0.0) 
    hiproll_drive.motor1.set_pos_setpoint(setpoint_right_roll+offset_right_roll, 0.0, 0.0)
    ankle_drive.motor0.set_pos_setpoint(setpoint_left_ankle+offset_left_ankle,0.0,0.0)
    ankle_drive.motor1.set_pos_setpoint(setpoint_right_ankle+offset_right_ankle,0.0,0.0)
    i = i + 1

    time.sleep(0.01)

def return_all_to_initial_position():
    left_hip_drive.motor1.set_pos_setpoint(offset_left_pitch, 0.0, 0.0)
    left_hip_drive.motor0.set_pos_setpoint(offset_left_slide, 0.0, 0.0)
    right_hip_drive.motor1.set_pos_setpoint(offset_right_slide, 0.0, 0.0)
    right_hip_drive.motor0.set_pos_setpoint(offset_right_slide, 0.0, 0.0)
    hiproll_drive.motor0.set_pos_setpoint(offset_left_roll, 0.0, 0.0) 
    hiproll_drive.motor1.set_pos_setpoint(offset_right_roll, 0.0, 0.0)
    ankle_drive.motor0.set_pos_setpoint(offset_left_ankle,0.0,0.0)
    ankle_drive.motor1.set_pos_setpoint(offset_right_ankle,0.0,0.0)
