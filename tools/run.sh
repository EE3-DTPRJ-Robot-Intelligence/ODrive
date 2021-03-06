#!/bin/bash

echo "Writing the below to udev rules..."
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="1209", ATTR{idProduct}=="0d[0-9][0-9]", MODE="0666"' | sudo tee /etc/udev/rules.d/50-odrive.rules
sudo udevadm control --reload-rules && sudo service udev restart && sudo udevadm trigger

python3 trajectory.py
