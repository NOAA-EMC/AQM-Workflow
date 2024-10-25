#!/bin/bash
#
set -eux
#
# This utility is to replace configuration template with production settings before running ecflow workflow
# Usage:
#       cd $HOMEaqm/parm/config
#       vi aqm_nco_config.sh and modify General parameter
#       sh aqm_nco_config.sh
#
# General parameters must be modified by NCEP/NCO/SPA
#   Remove the remark and modify with running environment
## OPSROOT="/lfs/h2/emc/ptmp/jianping.huang/ecflow_aqm/para"
## COMROOT="/lfs/h2/emc/ptmp/jianping.huang/ecflow_aqm/para/com"

## CONFIGURABLE VARIABLES
WARMSTART_PDY="20240128"
# [metadata]
description='config for Online-CMAQ, AQM_NA_13km, real-time, NCO mode on WCOSS2'
version='1.0'

# [user]
RUN_ENVIR='nco'
MACHINE='WCOSS2'

# [platform]
NCORES_PER_NODE='128'
BUILD_MOD_FN='build_wcoss2_intel'
WFLOW_MOD_FN='wflow_wcoss2'
BUILD_VER_FN='build.ver.wcoss2'
RUN_VER_FN='run.ver.wcoss2'
SCHED='pbspro'
RUN_CMD_UTILS='mpiexec -n ${nprocs}'
RUN_CMD_FCST='mpiexec -n ${PE_MEMBER01} -ppn ${PPN_RUN_FCST} --cpu-bind core -depth ${OMP_NUM_THREADS_RUN_FCST}'
RUN_CMD_POST='mpiexec -n ${nprocs}'
RUN_CMD_PRDGEN='mpiexec -n ${nprocs} --cpu-bind core cfp'
RUN_CMD_AQM='mpiexec -n ${nprocs} -ppn ${ppn_run_aqm} --cpu-bind core -depth ${omp_num_threads_run_aqm}'
RUN_CMD_AQMLBC='mpiexec -n ${NUMTS}'
SCHED_NATIVE_CMD='-l place=excl'

# [workflow]
WORKFLOW_ID='id_1697644234'
USE_CRON_TO_RELAUNCH='TRUE'
DIAG_TABLE_TMPL_FN='diag_table_aqm.FV3_GFS_v16'
FIELD_TABLE_TMPL_FN='field_table_aqm.FV3_GFS_v16'
DIAG_TABLE_TMPL_FP='${HOMEaqm}/parm/diag_table_aqm.FV3_GFS_v16'
FIELD_TABLE_TMPL_FP='${HOMEaqm}/parm/field_table_aqm.FV3_GFS_v16'
CCPP_PHYS_SUITE='FV3_GFS_v16'
CCPP_PHYS_SUITE_FN='suite_FV3_GFS_v16.xml'
CCPP_PHYS_SUITE_IN_CCPP_FP='${HOMEaqm}/sorc/ufs-weather-model/FV3/ccpp/suites/suite_FV3_GFS_v16.xml'
CCPP_PHYS_SUITE_FP='${HOMEaqm}/parm/config/suite_FV3_GFS_v16.xml'
PREDEF_GRID_NAME='AQM_NA_13km'
DATE_FIRST_CYCL='202310180000'
DATE_LAST_CYCL='209910181800'
INCR_CYCL_FREQ='6'
FCST_LEN_HRS='-1'
FCST_LEN_CYCL=( "6" "72" "72" "6" )
RESTART_INTERVAL='6 12 18 24 30 36 42 48 54 60 66'
VERBOSE='TRUE'
DEBUG='FALSE'
COMPILER='intel'
SYMLINK_FIX_FILES='FALSE'
DO_REAL_TIME='TRUE'
COLDSTART='FALSE'
WARMSTART_CYCLE_DIR='${COMaqm}/aqm.${WARMSTART_PDY}/18'
RES_IN_FIXLAM_FILENAMES='793'
CRES='C793'
SDF_USES_RUC_LSM='FALSE'
SDF_USES_THOMPSON_MP='FALSE'

# [workflow_switches]
RUN_TASK_MAKE_GRID='FALSE'
RUN_TASK_MAKE_OROG='FALSE'
RUN_TASK_MAKE_SFC_CLIMO='FALSE'
RUN_TASK_GET_EXTRN_ICS='FALSE'
RUN_TASK_GET_EXTRN_LBCS='FALSE'
RUN_TASK_MAKE_ICS='TRUE'
RUN_TASK_MAKE_LBCS='TRUE'
RUN_TASK_RUN_FCST='TRUE'
RUN_TASK_RUN_POST='TRUE'
RUN_TASK_RUN_PRDGEN='FALSE'
RUN_TASK_GET_OBS_CCPA='FALSE'
RUN_TASK_GET_OBS_MRMS='FALSE'
RUN_TASK_GET_OBS_NDAS='FALSE'
RUN_TASK_VX_GRIDSTAT='FALSE'
RUN_TASK_VX_POINTSTAT='FALSE'
RUN_TASK_VX_ENSGRID='FALSE'
RUN_TASK_VX_ENSPOINT='FALSE'
RUN_TASK_PLOT_ALLVARS='FALSE'
RUN_TASK_AQM_ICS='TRUE'
RUN_TASK_AQM_LBCS='TRUE'
RUN_TASK_NEXUS_GFS_SFC='FALSE'
RUN_TASK_NEXUS_EMISSION='TRUE'
RUN_TASK_FIRE_EMISSION='TRUE'
RUN_TASK_POINT_SOURCE='TRUE'
RUN_TASK_PRE_POST_STAT='TRUE'
RUN_TASK_POST_STAT_O3='TRUE'
RUN_TASK_POST_STAT_PM25='TRUE'
RUN_TASK_BIAS_CORRECTION_O3='TRUE'
RUN_TASK_BIAS_CORRECTION_PM25='TRUE'

#####################################################################################
# No need to modify any line below
#####################################################################################

# Target files to modify
File_to_modify_source="var_defns.sh"

# Source run.ver
source "$HOMEaqm/versions/run.ver" || { echo "Failed to source run.ver"; exit 1; }

# Assign COMaqm using production utility
## COMROOT=${COMROOT:-"${OPSROOT}/com"}
OPSROOT=$(realpath ${COMROOT}/..)
COMaqm=$(compath.py -o "aqm/${aqm_ver}") || { echo "Failed to assign COMaqm"; exit 1; }
COMINgefs=$(compath.py "gefs/${gefs_ver}") || { echo "Failed to assign COMINgefs"; exit 1; }
MODEL_VER_DFV=${COMaqm:(-4)}

# Replace special characters 
OPSROOT=$(printf '%q' "$OPSROOT")
HOMEaqm=$(printf '%q' "$HOMEaqm")
COMROOT=$(printf '%q' "$COMROOT")
DCOMROOT=$(printf '%q' "$DCOMROOT")
COMaqm=$(printf '%q' "$COMaqm")
COMINgefs=$(printf '%q' "$COMINgefs")
DATA=$(printf '%q' "$DATA")
MODEL_VER_DFV=$(printf '%q' "$MODEL_VER_DFV")

# Dynamically generate target files
cd "$DATA" || { echo "Failed to change directory to $DATA"; exit 1; }

#
source ${HOMEaqm}/ush/configurable_variables.sh
for file_in in ${File_to_modify_source}; do
  cp "$HOMEaqm/parm/config/${file_in}.template" .
  file_src="${file_in}.template"
  file_tmp=$(mktemp -p .) || { echo "Failed to create temporary file"; exit 1; }
  cp "$file_src" "$file_tmp" || { echo "Failed to copy $file_src to $file_tmp"; exit 1; }
  for variable in "${configurable_variables[@]}"; do
    if [ ! -z "${variable+x}" ]; then #CHECK IF VARIABLE IS SET ALREADY SO IT CAN SET IT IN THE TEMPLATE. (SET ABOVE)
      sed -i -e "s|@${variable}@|${!variable}|g" "${file_tmp}"
    fi
  done
  mv "$file_tmp" "$file_in" || { echo "Failed to move $file_tmp to $file_in"; exit 1; }
done
. $DATA/var_defns.sh 

exit 1
