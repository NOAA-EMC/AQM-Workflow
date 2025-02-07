#! /bin/bash
source user_settings.sh

cd ${workflow_dir}

if [[ -d ${fixdir} ]]; then
  ln -s ${fixdir} .
fi

cd sorc
bash auto_A1_checkout.sh
bash auto_A2_build_exec.sh
cd ..

cd ecf
bash setup_ecf_links.sh
cd ..

if [[ ! -d ${workflow_dir}/ecf/defs/submit ]]; then
  echo "Creating submit dir for workflow"
  mkdir ${workflow_dir}/ecf/defs/submit
fi
if [[ ! -d ${ptmpdir}/ecflow_aqm/para/com ]]; then
  echo "Making para/com dir for workflow"
  mkdir -p ${ptmpdir}/ecflow_aqm/para/com
fi
