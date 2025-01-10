#! /bin/bash

ln -s /lfs/h2/emc/physics/noscrub/UFS_SRW_App/aqm.v8.0/fix .

cd sorc
bash auto_A1_checkout.sh
bash auto_A2_build_exec.sh
cd ..

cd ecf
bash setup_ecf_links.sh
cd ..
