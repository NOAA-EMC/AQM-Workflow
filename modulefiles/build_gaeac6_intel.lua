help([[
This module loads libraries for building the UFS SRW App on
the NOAA RDHPC machine Gaea C5 using Intel-2023.1.0
]])

whatis([===[Loads libraries needed for building the AQM Workflow on Gaea C6 ]===])

prepend_path("MODULEPATH", "/ncrc/proj/epic/spack-stack/c6/spack-stack-1.9.2/envs/ue-intel-2023.2.0/install/modulefiles/Core")

stack_intel_ver=os.getenv("stack_intel_ver") or "2023.2.0"
load(pathJoin("stack-intel", stack_intel_ver))

stack_mpich_ver=os.getenv("stack_mpich_ver") or "8.1.30"
load(pathJoin("stack-cray-mpich", stack_mpich_ver))

-- craype_ver=os.getenv("craype_ver") or "2.7.34"
-- load(pathJoin("craype", craype_ver))

stack_python_ver=os.getenv("stack_python_ver") or "3.11.7"
load(pathJoin("stack-python", stack_python_ver))

cmake_ver=os.getenv("cmake_ver") or "3.27.9"   
load(pathJoin("cmake", cmake_ver))

local aqm_modules = {
    {["bacio"]          = "2.4.1"},
    {["bufr"]           = "12.1.0"},
    {["crtm"]           = "2.4.0.1"},
    {["esmf"]           = "8.8.0"},
    {["fms"]            = "2024.02"},
    {["g2"]             = "3.5.1"},
    {["g2tmpl"]         = "1.13.0"},
    {["gftl-shared"]    = "1.9.0"},
    {["hdf5"]           = "1.14.3"},
    {["ip"]             = "5.1.0"},
    {["jasper"]         = "2.0.32"},
    {["libpng"]         = "1.6.37"},
    {["mapl"]           = "2.53.4-esmf-8.8.0"},
    {["nccmp"]          = "1.9.0.1"},
    {["nco"]            = "5.2.4"},
    {["nemsio"]         = "2.5.4"},
    {["netcdf-c"]       = "4.9.2"},
    {["netcdf-fortran"] = "4.6.1"},
    {["parallelio"]     = "2.6.2"},
    {["prod_util"]      = "2.1.1"},
    {["scotch"]         = "7.0.4"},
    {["sfcio"]          = "1.4.2"},
    {["sigio"]          = "2.3.3"},
    {["sp"]             = "2.5.0"},
    {["w3emc"]          = "2.10.0"},
    {["w3nco"]          = "2.4.1"},
    {["wgrib2"]         = "3.6.0"},
    {["wrf-io"]         = "1.2.0"},
    {["zlib"]           = "1.2.13"},
}

for i = 1, #aqm_modules do
  for name, default_version in pairs(aqm_modules[i]) do
    local env_version_name = string.gsub(name, "-", "_") .. "_ver"
    load(pathJoin(name, os.getenv(env_version_name) or default_version))
  end
end

prepend_path("MODULEPATH", "/ncrc/proj/epic/spack-stack/modulefiles")
load("ecflow")

unload("darshan-runtime")
unload("cray-libsci")

setenv("CC","cc")
setenv("CXX","CC")
setenv("FC","ftn")

setenv("CMAKE_C_COMPILER","cc")
setenv("CMAKE_Fortran_COMPILER","ftn")
setenv("CMAKE_CXX_COMPILER","CC")
setenv("CMAKE_Platform","gaea.intel")
