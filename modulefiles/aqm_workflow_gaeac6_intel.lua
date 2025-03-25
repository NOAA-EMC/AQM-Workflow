whatis([===[Loads libraries & modules needed for AQM_Workflow on GaeaC6]===])

prepend_path("MODULEPATH", "/ncrc/proj/epic/spack-stack/c6/spack-stack-1.6.0/envs/fms-2024.01/install/modulefiles/Core")

load(pathJoin("stack-python", "3.10.13"))
load(pathJoin("py-pyyaml", "6.0"))
load(pathJoin("ecflow", "5.11.4"))
