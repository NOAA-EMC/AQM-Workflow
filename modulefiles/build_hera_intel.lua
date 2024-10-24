help([[
This module loads libraries for building the SRW workflow on
the NOAA RDHPC machine Hera using Intel-2022.1.2
]])

whatis([===[Loads libraries needed for building the SRW workflow on Hera ]===])

prepend_path("MODULEPATH", "/scratch1/NCEPDEV/nems/role.epic/spack-stack/spack-stack-1.6.0/envs/fms-2024.01/install/modulefiles/Core")
--prepend_path("MODULEPATH", "/scratch1/NCEPDEV/jcsda/jedipara/spack-stack/modulefiles")

load(pathJoin("stack-intel", "2021.5.0"))
load(pathJoin("stack-intel-oneapi-mpi", "2021.5.1"))
load(pathJoin("stack-python", "3.10.13"))

--does it need to be 3.23.1 like ufswm?
load(pathJoin("cmake", "3.28.1"))

load(pathJoin("hdf5", "1.14.0"))
load(pathJoin("netcdf-c", "4.9.2"))
load(pathJoin("netcdf-fortran", "4.6.1"))
load(pathJoin("parallelio", "2.5.10"))
load(pathJoin("esmf", "8.6.0"))
load(pathJoin("fms", "2024.01"))
load(pathJoin("crtm", "2.4.0.1"))
load(pathJoin("mapl", "2.40.3-esmf-8.6.0"))
load(pathJoin("scotch", "7.0.4"))
load(pathJoin("nemsio", "2.5.4"))
--load(pathJoin("nemsiogfs", "2.5.3"))
load(pathJoin("wrf-io", "1.2.0"))
--load(pathJoin("ncio", "1.1.2"))
load(pathJoin("nccmp", "1.9.0.1"))
load(pathJoin("nco", "5.0.6"))

load(pathJoin("jasper", "2.0.32"))
load(pathJoin("zlib", "1.2.13"))
load(pathJoin("libpng", "1.6.37"))
load(pathJoin("bacio", "2.4.1"))
load(pathJoin("g2", "3.5.1"))
load(pathJoin("g2tmpl", "1.13.0"))
load(pathJoin("ip", "4.3.0"))
load(pathJoin("sp", "2.5.0"))
load(pathJoin("gftl-shared", "1.6.1"))
load(pathJoin("bufr", "12.0.1"))
--load(pathJoin("gfsio", "1.4.1"))
--load(pathJoin("landsfcutil", "2.4.1"))
load(pathJoin("sigio", "2.3.2"))
load(pathJoin("sfcio", "1.4.1"))
load(pathJoin("w3emc", "2.10.0"))
load(pathJoin("w3nco", "2.4.1"))
--load(pathJoin("prod_util", "1.2.2")) ufswm uses 2.1.1
load(pathJoin("prod_util", "2.1.1"))
load(pathJoin("wgrib2", "2.0.8"))


prepend_path("MODULEPATH", "/scratch2/BMC/ifi/modulefiles")
try_load("ifi/20230511-intel-2022.1.2")

setenv("CMAKE_C_COMPILER","mpiicc")
setenv("CMAKE_CXX_COMPILER","mpiicpc")
setenv("CMAKE_Fortran_COMPILER","mpiifort")
setenv("CMAKE_Platform","hera.intel")
