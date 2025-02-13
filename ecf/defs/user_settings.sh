#!/bin/bash

# Please fill out the following paths and settings to fit your preferences

# You can set this in case you don't want to use this dir
export workflow_dir=${workflow_dir:-${PWD}}
echo "Workflow dir: ${workflow_dir}"

# group to use for workflow
export user_group=physics

# ECFlow Host Server Location
# Can be left blank if set by module load properly
module load ecflow
export ECF_HOST=cdecflow01

# Location/path for ecflow files
#export ecflow_dir=/lfs/h2/emc/${user_group}/noscrub/${USER}/ecflow
export ecflow_dir=/lfs/h2/emc/physics/noscrub/anna.smoot/git/AnnaSmoot-NOAA/AQM-Workflow/ecflow_fixes/AQM-Workflow/ecf/defs

# Which mode will you be generating the workflow for?
# realtime? retro?
export workflow_mode=realtime

#What version of AQM are you using? Default is v8.0.1.
export aqm_ver=v8.0.1

#What's the start date? 
export PDY=20230701

#How many cycles do you want to run? (choose 00, 06, 12, or 18)
export CYC=00

#WCOSS2 only settings:
export PROJ=AQM
export PROJENV=DEV
export NET=aqm
export RUN=aqm
export ENVIR=dev

#Initiate Python:
export MACHINE_SITE=
export QUEUE= 
export QUEUE_ARCH=
export PACKAGEHOME=/lfs/h2/emc/physics/noscrub/%EMC_USER%/nwdev/packages/aqm.%aqm_ver%
export OUTPUTDIR=/lfs/h2/emc/ptmp/%EMC_USER%/ecflow_aqm/para/output/prod/today

#Python definition generation script
python aqm_cyc_test.py
