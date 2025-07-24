whatis([===[Loads libraries & modules needed for AQM_Workflow on Hera]===])

prepend_path("MODULEPATH", "/scratch1/NCEPDEV/nems/role.epic/spack-stack/spack-stack-1.6.0/envs/fms-2024.01/install/modulefiles/Core")

load(pathJoin("stack-python", "3.10.13"))
load(pathJoin("ecflow", "5.11.4"))
load(pathJoin("py-pyyaml","6.0"))
