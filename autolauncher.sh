#!/bin/bash
# Set the system volume and start the clock code
amixer sset 'Master' 75%
python3 /home/pi-clock/clock_code/pi_clock.py --limit-changes --chime-type modern