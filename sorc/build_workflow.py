import subprocess
import os
import argparse
    
def parse_arguments():
    # Get some system info to use in setting up defaults for argparse
    sorc_dir = os.getcwd()
    workflow_dir = os.path.dirname(sorc_dir)

    parser = argparse.ArgumentParser(description="Build the AQM Workflow")
    
    parser.add_argument("--build-all", action="store_true")
    parser.add_argument("--build-ufs", action="store_true")
    parser.add_argument("--build-ufs-utils", action="store_true")
    parser.add_argument("--build-aqm-utils", action="store_true")
    parser.add_argument("--build-nexus", action="store_true")
    parser.add_argument("--build-upp", action="store_true")
    parser.add_argument("-c", "--compiler", nargs=1, type=str, default="Intel")
    parser.add_argument("--ccpp-suites", nargs="?", type=str, default="FV3_GFS_v16")
    #parser.add_argument(--enable-options=?*) ENABLE_OPTIONS=${1#*=} ;;
    #parser.add_argument(--disable-options=?*) DISABLE_OPTIONS=${1#*=} ;;
    parser.add_argument("--remove", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--build", action="store_true")
    #parser.add_argument("--move", action="store_true")
    parser.add_argument("--build-dir", nargs=1, type=str, default=f'{sorc_dir}/build')
    parser.add_argument("--install-dir", nargs=1, type=str, default=f'{sorc_dir}/build')
    #parser.add_argument("--bin-dir")
    parser.add_argument("--build-type", nargs=1, type=str, default="Release")
    parser.add_argument("--build-jobs", nargs=1, type=int, default=4)
    parser.add_argument("-v", "--verbose", action="store_true")
    #parser.add_argument("--use-sub-modules")

    return parser.parse_args()

class ArgValidaton:
    
    def __init__(self, args):
        self.subcomponent(args)
        self.directories(args)
        self.options(args)

    def options(self, args):
        self.remove: bool = args.remove
        self.resume: bool = args.resume
        self.clean: bool = args.clean
        self.build: bool = args.build
        self.build_type: str = args.build_type
        self.build_jobs: int = args.build_jobs
        self.verbose: bool = args.verbose

    def directories(self, args):
        self.build_dir: str = args.build_dir
        self.install_dir: str = args.install_dir

    def subcomponent(self, args):
        self.build_all: bool = args.build_all
        self.build_ufs: bool = args.build_ufs
        self.build_ufs_utils: bool = args.build_ufs_utils
        self.build_aqm_utils: bool = args.build_aqm_utils
        self.build_nexus: bool = args.build_nexus
        self.build_upp: bool = args.build_upp

        if self.build_all:
            self.build_ufs = True
            self.build_ufs_utils = True
            self.build_aqm_utils = True
            self.build_nexus = True
            self.build_upp = True

def do_build_ufs():
    print("Building UFS")
    pass

def do_build_ufs_utils(validated_args):
    print("Building UFS_UTILS")

    # Build UFS utilities

    ufs_utils_cmake_call_pre: List[str] = [
        "cmake",
        "-S",
        "UFS_UTILS",
        "-B",
        f"{validated_args.build_dir}/UFS_UTILS"
    ]

    ufs_utils_cmake_args: List[str] = [
        #f"-DCMAKE_INSTALL_PREFIX={os.environ['CMAKE_INSTALL_PREFIX']}",
        #f"-DCMAKE_INSTALL_BINDIR={os.environ['CMAKE_INSTALL_BINDIR']}",
        f"-DCMAKE_BUILD_TYPE={validated_args.build_type}",
        "-DBUILD_TESTING=OFF",
        "-DFRENCTOOLS=OFF",
        "-DICEBLEND=OFF",
        "-DSNOW2MDL=OFF",
        "-DGCYCLE=OFF",
        "-DGRIDTOOLS=OFF",
        "-DOROG_MASK_TOOLS=OFF",
        "-DSFC_CLIMO_GEN=OFF",
        "-DVCOORD_GEN=OFF",
        "-DFVCOMTOOLS=OFF",
        "-DGBLEVENTS=OFF",
        "-DOCEAN_MERGE=OFF",
        "-DCPLD_GRIDGEN=OFF",
        "-DWEIGHT_GEN=OFF"
        ]
    
    print(ufs_utils_cmake_call_pre + ufs_utils_cmake_args)
    subprocess.run(ufs_utils_cmake_call_pre + ufs_utils_cmake_args)
    print(["make", "-C", f"{validated_args.build_dir}/UFS_UTILS"])
    subprocess.run(["make", "-C", f"{validated_args.build_dir}/UFS_UTILS"])

    pass

def do_build_aqm_utils():
    print("Building AQM_UTILS")
    pass

def do_build_nexus():
    print("Building NEXUS")
    pass

def do_build_upp():
    print("Building UPP")
    pass

def main():
    args = parse_arguments()
    validated_args = ArgValidaton(args)
    
    do_build_ufs() if validated_args.build_ufs else print("Skipping UFS Build")
    do_build_ufs_utils(validated_args) if validated_args.build_ufs_utils else print("Skipping UFS_UTILS Build")
    do_build_aqm_utils() if validated_args.build_aqm_utils else print("Skipping AQM_UTILS Build")
    do_build_nexus() if validated_args.build_nexus else print("Skipping NEXUS Build")
    do_build_upp() if validated_args.build_upp else print("Skipping UPP Build")

if __name__ == "__main__":
    main()