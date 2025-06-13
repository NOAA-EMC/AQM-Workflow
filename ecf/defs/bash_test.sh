 #!/bin/bash -l

#export VAR1="Hello, world!"
#export VAR2=42

#echo "VAR1 is: ${VAR1}"
#echo "VAR2 is: ${VAR2}"

#get detect_machine.sh 
echo "Executing detect_machine.sh using source."
source detect_machine.sh
export MACHINE_ID
echo "MACHINE_ID from detect_machine.sh: $MACHINE_ID"

#run module-setup.sh
#echo "Executng module-setup.sh using source." 
#source module-setup.sh
#export MACHINE_ID
#echo "From module-setup.sh: $MACHINE_ID"

#get user_settings.sh
#echo "Executing user_settings.sh using source." 
#source user_settings.sh
#echo "PDY from user_settings.sh: $PDY"

#python machine_test.py
#python ecf_host_test.py
