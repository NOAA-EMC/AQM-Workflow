#!/bin/bash

# Please fill out the following paths and settings to fit your preferences

# You can set this in case you don't want to use this dir

MACHINE_ID=gaeac6
export MACHINE_ID
workflow_dir=${workflow_dir:-${PWD}}
export workflow_dir
echo "Workflow dir: ${workflow_dir}"

# group to use for workflow
export user_group=drsa-fire2

# Location/path for ecflow files
if [[ ${MACHINE_ID} == wcoss2 ]]; then
    export fixdir=/lfs/h2/emc/physics/noscrub/UFS_SRW_App/aqm.v8.0/fix
    export ptmpdir=/lfs/h2/emc/ptmp
    export ecflow_dir=/lfs/h2/emc/${user_group}/noscrub/${USER}/ecflow
elif [[ ${MACHINE_ID} == gaeac6 ]]; then
    export fixdir=/gpfs/f6/drsa-fire2/world-shared/AQM-Data/fix
    export ptmpdir=/gpfs/f6/drsa-fire2/scratch
    export ecflow_dir=/gpfs/f6/drsa-fire2/scratch/${USER}/ecflow
fi

# Which mode will you be generating the workflow for?
# realtime? retro?
export workflow_mode=realtime

export PTMP=${ptmpdir}
export STMP=${PTMP}
# export DATAROOT=${PTMP}/${USER}/aqm/ecflow_aqm
# #export COMROOT=${PTMP}/ecflow_aqm/para/com
# export COMROOT=/gpfs/f6/drsa-fire2/world-shared/AQM-Data/com
#export COMOUT=/gpfs/f6/drsa-fire2/world-shared/AQM-Data/com/aqm/v8.0/aqm.20230701
export COMOUT=${ptmpdir}/${USER}/ecflow_aqm/para/com/aqm/v8.0/aqm.20230701
export COMIN=/gpfs/f6/drsa-fire2/world-shared/AQM-Data/com/aqm/v8.0/aqm.20230701
export DCOMROOT=/gpfs/f6/drsa-fire2/world-shared/AQM-Data/dcom
# export COMPATH=${PTMP}/${USER}/ecflow_aqm/para/com/aqm
# RUN_ENVIR typically 'nco' or 'dev'
export RUN_ENVIR=dev
# export PDY=20230701
# export COMINgefs=/gpfs/f6/drsa-fire2/world-shared/AQM-Data/com/gefs/v12.3
# export COMINgfs=/gpfs/f6/drsa-fire2/world-shared/AQM-Data/com/gfs/v16.3
