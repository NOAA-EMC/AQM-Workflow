#! /bin/bash

module load ecflow
export ECF_PORT=${ECF_PORT}
export ECF_HOST=ddecflow01
export ECF_HOME=/lfs/h2/emc/nems/noscrub/${USER}/ecflow/submit
export ECF_DATA_ROOT=/lfs/h2/emc/nems/noscrub/${USER}/ecflow
export ECF_OUTPUTDIR=/lfs/h2/emc/nems/noscrub/${USER}/ecflow/output
export ECF_COMDIR=/lfs/h2/emc/nems/noscrub/${USER}/ecflow/submit
export LFS_OUTPUTDIR=/lfs/h2/emc/nems/noscrub/${USER}/ecflow/submit
export ECF_LISTS=${ECF_HOST}.${ECF_PORT}.ecf.lists
