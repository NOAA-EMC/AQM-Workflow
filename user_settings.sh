#!/bin/bash

# Please fill out the following paths and settings to fit your preferences

# You can set this in case you don't want to use this dir
export workflow_dir=${workflow_dir:-${PWD}}
echo "Workflow dir: ${workflow_dir}"

# group to use for workflow
export user_group=nems

# ECFlow Host Server Location
# Can be left blank if set by module load properly
module load ecflow
export ECF_HOST=cdecflow01

# Location/path for ecflow files
export fixdir=/lfs/h2/emc/physics/noscrub/UFS_SRW_App/aqm.v8.0/fix
export ptmpdir=/lfs/h2/emc/ptmp/${USER}
export ecflow_dir=/lfs/h2/emc/${user_group}/noscrub/${USER}/ecflow

# Which mode will you be generating the workflow for?
# realtime? retro?
export workflow_mode=realtime
