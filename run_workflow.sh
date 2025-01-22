#! /bin/bash

# Load ECFLOW
module load ecflow

# Bring in user settings
# source user_settings.sh
# source setup_ecflow.sh

server_check.sh

ecflow_client --delete=force yes /aqm_test

ecflow_client --load ecf/defs/aqm_testing.def # This should he soft_coded to use variable 'aqm_${workflow_mode}.def'

ecflow_client --begin /aqm_test #This should be soft coded to use a variable 'suite_name'

ecflow_ui &
