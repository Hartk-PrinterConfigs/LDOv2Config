#!/bin/bash
IP=$(hostname -I)
echo M117 $IP > ~/gcode_files/ip.gcode


