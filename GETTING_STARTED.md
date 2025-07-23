STEPS TO GET WORKFLOW RUNNING (FOR NOW)
If using Ecflow, make sure you have Xming or some x window loaded, ssh -X to an ecflow node before starting.
 * module use modulefiles/
 * module load build_wcoss2_intel OR module load build_gaeac6_intel
 * module load aqm_workflow_wcoss2_intel OR module load aqm_workflow_gaeac6_intel
 * python -c 'import ecflow'
 * python -c 'import yaml'
 * cd ush/
 * cat GETTING_STARTED.md in ush
