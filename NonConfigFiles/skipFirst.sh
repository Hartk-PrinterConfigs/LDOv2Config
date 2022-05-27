#!/bin/bash

  cd ~/klipper
  git remote add probe-drop-first https://github.com/hifihedgehog/klipper.git
  git fetch probe-drop-first
  git cherry-pick ad23f41ce542b8a637ef91a57dad5d4e2ee7b6f1
  sudo service klipper restart

echo M117 Skip First Probe updated > /tmp/printer