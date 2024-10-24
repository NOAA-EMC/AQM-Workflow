help([[
This module loads libraries for building the UFS SRW App on
the NOAA RDHPC machine Gaea C5 using Intel-2023.1.0
]])

whatis([===[Loads libraries needed for building the UFS SRW App on Gaea C5 ]===])


--prepend_path("MODULEPATH", "/ncrc/proj/epic/spack-stack/spack-stack-1.6.0/envs/upp-addon-env/install/modulefiles/Core")
prepend_path("MODULEPATH", "/ncrc/proj/epic/spack-stack/c6/spack-stack-1.6.0/envs/upp-addon-env/install/modulefiles/Core")

stack_intel_ver=os.getenv("stack_intel_ver") or "2023.2.0"
load(pathJoin("stack-intel", stack_intel_ver))

stack_mpich_ver=os.getenv("stack_mpich_ver") or "8.1.29"
load(pathJoin("stack-cray-mpich", stack_mpich_ver))

stack_python_ver=os.getenv("stack_python_ver") or "3.10.13"
load(pathJoin("stack-python", stack_python_ver))

--cmake_ver=os.getenv("cmake_ver") or "3.27.9"
--cmake_ver=os.getenv("cmake_ver") or "3.23.1"   
cmake_ver=os.getenv("cmake_ver") or "3.23.1"   
load(pathJoin("cmake", cmake_ver))

--load("srw_common")
--instead load the lib versions that work on latest AQM Hera lua, but in srw_common order

load(pathJoin("jasper", "2.0.32"))
load(pathJoin("zlib", "1.2.13"))
load(pathJoin("libpng", "1.6.37"))

load(pathJoin("netcdf-c", "4.9.2"))
load(pathJoin("netcdf-fortran", "4.6.1"))
load(pathJoin("parallelio", "2.5.10"))
load(pathJoin("esmf", "8.6.0"))
--load(pathJoin("fms", "2024.01")) --srw has 2023.04
load(pathJoin("fms", "2023.04"))

load(pathJoin("bacio", "2.4.1"))
load(pathJoin("crtm", "2.4.0.1"))
load(pathJoin("g2", "3.5.1"))
load(pathJoin("g2tmpl", "1.13.0"))
load(pathJoin("ip", "4.3.0"))
load(pathJoin("sp", "2.5.0"))
load(pathJoin("w3emc", "2.10.0"))

load(pathJoin("gftl-shared", "1.6.1"))
load(pathJoin("mapl", "2.40.3-esmf-8.6.0"))

load(pathJoin("nemsio", "2.5.4"))
load(pathJoin("sfcio", "1.4.1"))
load(pathJoin("sigio", "2.3.2"))
load(pathJoin("w3nco", "2.4.1"))
load(pathJoin("wrf-io", "1.2.0"))

--from AQM  hera.lua but not used in srw app luas
--commented out lines may need to come back when generating wflow
load(pathJoin("hdf5", "1.14.0"))
load(pathJoin("scotch", "7.0.4"))
--load(pathJoin("nemsiogfs", "2.5.3"))
--load(pathJoin("ncio", "1.1.2"))
load(pathJoin("nccmp", "1.9.0.1"))
load(pathJoin("nco", "5.0.6"))
load(pathJoin("bufr", "12.0.1")) --srw has 12.0.32
--load(pathJoin("gfsio", "1.4.1"))
--load(pathJoin("landsfcutil", "2.4.1"))
load(pathJoin("prod_util", "2.1.1"))
load(pathJoin("wgrib2", "2.0.8"))

--AQM hera.lua does not have these 
unload("darshan-runtime/3.4.0")
unload("cray-pmi/6.1.10")

setenv("CFLAGS","-diag-disable=10441")
setenv("FFLAGS","-diag-disable=10441")

setenv("CC","cc")
setenv("FC","ftn")
setenv("CXX","CC")

--same as AQM hera.lua
setenv("CMAKE_C_COMPILER","cc")
setenv("CMAKE_Fortran_COMPILER","ftn")
setenv("CMAKE_CXX_COMPILER","CC")
setenv("CMAKE_Platform","gaea.intel")
