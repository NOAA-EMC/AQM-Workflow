#! /bin/bash
#
# This is the setup script for AQM Workflow.
# It currently only applies to WCOSS2.
# Please develop this script knowing it will eventually apply to multiple systems.

# Bring in user settings
source user_settings.sh

# ECFlow Server Settings
export ECF_HOST=${ECF_HOST:-}
export ECF_PORT=${ECF_PORT:-}

# ECFlow Settings
export ECF_DATA_ROOT=${ecflow_dir}
export ECF_OUTPUTDIR=${ecflow_dir}/output
export ECF_COMDIR=${ecflow_dir}/submit
export LFS_OUTPUTDIR=${ECF_COMDIR}
export ECF_LISTS={ECF_HOST}.{ECF_PORT}.ecf.lists
export ECF_INCLUDE=${workflow_dir}/ecf/include
