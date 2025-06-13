#Test of python using detecting machine bash script

#Imports
import ecflow as ecf
import os

#main function
def main():
    get_machine()
#    get set_up()
    get_settings()

#Read machine_detect.sh
#https://github.com/ufs-community/ufs-weather-model/blob/develop/tests/detect_machine.sh
#def get_machine_script(file_path):

#source detect_machine.sh
def get_machine():
    print(f"From python script MACHINE_ID:", os.environ.get('MACHINE_ID'))

#source module-setup.sh
#def get_setup():
#    print(f"From python script MACHINE_ID", os.environ.get("MACHINE_ID"))

#source user_settings.sh
def get_settings():
    print(f"From python script PDY:", os.environ.get('PDY'))

main()