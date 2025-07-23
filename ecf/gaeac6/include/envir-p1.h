# envir-p1.h
export job=${job:-%TASK%}
export jobid=${jobid:-${job}}

export RUN_ENVIR=${RUN_ENVIR:-nco}
export envir=%ENVIR%
export MACHINE_SITE=%MACHINE_SITE%
export RUN=%RUN%

if [ -n "%SENDCANNEDDBN:%" ]; then export SENDCANNEDDBN=${SENDCANNEDDBN:-%SENDCANNEDDBN:%}; fi
export SENDCANNEDDBN=${SENDCANNEDDBN:-"NO"}

if [[ "$envir" == prod && "$SENDDBN" == YES ]]; then
    export eval=%EVAL:NO%
    if [ $eval == YES ]; then export SIPHONROOT=${UTILROOT}/para_dbn
    else export SIPHONROOT=/lfs/h1/ops/prod/dbnet_siphon
    fi
    if [ "$PARATEST" == YES ]; then export SIPHONROOT=${UTILROOT}/fakedbn; export NODBNFCHK=YES; fi
else
    export SIPHONROOT=${UTILROOT}/fakedbn
fi
export SIPHONROOT=${UTILROOT}/fakedbn
export DBNROOT=$SIPHONROOT

if [[ ! " prod para test " =~ " ${envir} " && " ops.prod ops.para " =~ " $(whoami) " ]]; then err_exit "ENVIR must be prod, para, or test [envir-p1.h]"; fi

# Developer configuration
PTMP=${PTMP:-}
STMP=${STMP:-}
if [ ! -d "$PTMP" ]; then
  echo "PTMP is not set or does not exist: $PTMP"
  echo "Please set PTMP to a valid temporary directory."
  exit 1
fi
if [ ! -d "$STMP" ]; then
  echo "STMP is not set or does not exist: $STMP"
  echo "Please set STMP to a valid temporary directory."
  exit 1
fi

model=${model:-aqm}
PSLOT=${PSLOT:-ecflow_aqm}
export COMROOT=${PTMP}/${USER}/${PSLOT}/para/com
export COMPATH=${COMROOT}/${model}
if [ -n "%PDY:%" ]; then
  export PDY=${PDY:-%PDY:%}
else
  export PDY=$($NDATE | cut -c1-8)
fi
export CDATE=${PDY}%CYC:%
export COMaqm=${COMaqm:-$(compath.py aqm/${aqm_ver})}
# export COMOUT_PREP="$(compath.py obsproc/v1.1.0)"

export DATAROOT=${DATAROOT:-${STMP}/${USER}/${model}/${PSLOT}}
mkdir -p ${DATAROOT} # ${COMaqm}

