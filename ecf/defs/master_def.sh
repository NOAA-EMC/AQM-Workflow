#!/bin/bash -l

#get detect_machine.sh
echo "Executing detect_machine.sh"
source detect_machine.sh
export MACHINE_ID
echo "MACHINE_ID from detect_machine.sh: $MACHINE_ID"

#get user_settings.sh
echo "Executing user_settings.sh"
source user_settings.sh
echo "PDY from user_settings.sh: $PDY"

python aqm_cyc_test.py
