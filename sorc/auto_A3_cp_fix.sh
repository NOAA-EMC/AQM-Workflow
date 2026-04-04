#!/bin/bash 
#
set -ax
#
export dev_fix=/lfs/h2/emc/physics/noscrub/AQM-Workflow/aqm.v8.0/fix
cd ../

export HOMEaqm=$(pwd)

cd $HOMEaqm

cp -rp ${dev_fix} .

