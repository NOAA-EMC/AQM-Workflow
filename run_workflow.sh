#! /bin/bash

# Load ECFLOW
module load ecflow
echo "MACHINEID: ${MACHINE_ID}"
if [[ ${MACHINE_ID} =~ wcoss2 ]]; then
  server_check.sh
elif [[ ${MACHINE_ID} =~ gaeac6 ]]; then
  # No Gaea ECFLOW nodes.
  export ECF_HOST=$(hostname)
  export ECF_PORT=$(( $(id -u ${USER}) + 1500 ))
elif [[ ${MACHINE_ID} =~ hera ]]; then
  echo "HERA HERA HERA HERA"
else
  echo "Unsupported System: Exiting"
  exit 1
fi

ecflow_client --delete=force yes /aqm_test

ecflow_client --load ecf/defs/aqm_testing.def # This should he soft_coded to use variable 'aqm_${workflow_mode}.def'

ecflow_client --begin /aqm_test #This should be soft coded to use a variable 'suite_name'

ecflow_ui &
