#!/bin/bash

#Please fill out the following paths and settings to fit your preferences

#You can set this in case you don't want to use this dir
workflow_dir=${workflow_dir:-${PWD}}
export workflow_dir
echo "Workflow dir: ${workflow_dir}"

#group to use for workflow
user_group=physics
export user_group

#ECFlow Host Server Location
#Can be left blank if set by module load properly
module load ecflow
ECF_HOST=cdecflow01
export ECF_HOST

#Location/path for ecflow files
#export ecflow_dir=/lfs/h2/emc/${user_group}/noscrub/${USER}/ecflow
ecflow_dir=/lfs/h2/emc/physics/noscrub/anna.smoot/git/AnnaSmoot-NOAA/AQM-Workflow/ecflow_fixes/AQM-Workflow/ecf/defs
export ecflow_dir

#Which mode will you be generating the workflow for?
#realtime? retro?
workflow_mode=realtime
export workflow_mode

#What version of AQM are you using? Default is v8.0.1.
aqm_ver=v8.0.1
export aqm_ver

#What's the start date? 
#export PDY=20230701
PDY=2023070120230701
export PDY

#How many cycles do you want to run? (choose 00, 06, 12, or 18)
CYC=00
export CYC

#WCOSS2 only settings:
PROJ=AQM
export PROJ
PROJENV=DEV
export PROJENV
NET=aqm
export NET
RUN=aqm
export RUN
ENVIR=dev
export ENVIR

#Initiate Python:
#MACHINE_SITE=
#export MACHINE_SITE
#QUEUE= 
#export QUEUE
#QUEUE_ARCH=
#export QUEUE_ARCH
PACKAGEHOME=/lfs/h2/emc/physics/noscrub/%EMC_USER%/nwdev/packages/aqm.%aqm_ver%
export PACKAGEHOME
OUTPUTDIR=/lfs/h2/emc/ptmp/%EMC_USER%/ecflow_aqm/para/output/prod/today
export OUTPUTDIR

#Python definition generation script
#python aqm_cyc_test.py
