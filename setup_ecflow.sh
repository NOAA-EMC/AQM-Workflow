#! /bin/bash
#
# This is the setup script for AQM Workflow.
# It currently only applies to WCOSS2.
# Please develop this script knowing it will eventually apply to multiple systems.

# Bring in user settings
source user_settings.sh

if [[ ${MACHINE_ID} =~ gaeac6 ]]; then
    module use /ncrc/proj/epic/spack-stack/modulefiles
fi
module load ecflow
# ECFlow Server Settings
export ECF_HOST=${ECF_HOST:-$(hostname)}
export ECF_PORT=${ECF_PORT:-$(( $(id -u ${USER}) + 1500 ))}

# ECFlow Settings
export ECF_DATA_ROOT=${ecflow_dir}
export ECF_OUTPUTDIR=${ecflow_dir}/output
export ECF_COMDIR=${ecflow_dir}/submit
export LFS_OUTPUTDIR=${ECF_COMDIR}
export ECF_LISTS=${ECF_HOST}.${ECF_PORT}.ecf.lists
export ECF_INCLUDE=${workflow_dir}/ecf/include
export ECF_HOME=${workflow_dir}
export ECF_OUT=${workflow_dir}
