#!/bin/bash:

# Please fill out the following paths and settings to fit your preferences

# You can set this in case you don't want to use this dir
export workflow_dir=$(realpath "${PWD}/..")
echo "Workflow dir: ${workflow_dir}"

# ECFlow Host Server Location
# Can be left blank if set by module load properly
module load ecflow
export ECF_HOST=cdecflow01

# Location/path for ecflow files
export fixdir=/lfs/h2/emc/physics/noscrub/UFS_SRW_App/aqm.v8.0/fix
export ptmpdir=/lfs/h2/emc/ptmp/${USER}
export ecflow_dir=/lfs/h2/emc/${user_group}/noscrub/${USER}/ecflow

# Which type of run do you want to generate?
# nco, test, or user?
# nco is for running the full operational suite
# test is for running one test cycle 
# user is customizable
export run_type=user
