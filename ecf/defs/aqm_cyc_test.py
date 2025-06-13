#This is a Python file to generate ecflow def files (test, NCO, and custom)
#It takes in variables from detect_machine.sh and user_settings.sh

#Imports
import ecflow as ecf
import os
#import yaml
import subprocess 

#main function
def main():
    get_machine()
    get_user_settings()
    defs = ecf.Defs()
    suite(defs)
    f_primary(defs)
    #f_cycle(defs)
    out_file(defs)

''' 
#BASH RUN VER: source user_settings.sh in the master_def.sh script 
def get_machine():
    print(f"From python script MACHINE_ID:", os.environ.get('MACHINE_ID'))

#BASH RUN VER: source user_settings.sh in the master_def.sh script 
##1. reads user_setting.sh, 2. checks vars exsist, 3. checks values are good
#commented out python call in user_settings.sh. Need to add this to run bash version
def get_user_settings():
    print(f"From python script PDY:", os.environ.get('PDY'))
'''

#PY RUN VER: This function runs detect_machine.sh
def get_machine():
    #run detect_machine.sh, dm = detect_machine
    dm_file_path = "/scratch2/NCEPDEV/naqfc/Anna.Smoot/git/AnnaSmoot-NOAA/AQM-Workflow/ecf_update/ecf/defs/detect_machine.sh"
    dm_process = subprocess.Popen(f'source {dm_file_path} && export MACHINE_ID && printenv | grep MACHINE', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    dm_stdout, dm_stderr = dm_process.communicate()

    if dm_process.returncode != 0:
        raise Exception(f"Error: {dm_stderr.decode()}")
    print(f"output: {dm_stdout.decode()}")

    #extract vars (MACHINE_ID)
    dm_env_vars = {}
    for line in dm_stdout.decode().splitlines():
        if "=" in line: 
            key, value = line.split("=", 1)
            dm_env_vars[key] = value
            print(f"dm_env_vars_out: {dm_env_vars}")
            return dm_env_vars

#PY RUN VER: runs user_settings.sh & gets exports 
def get_user_settings():
    #run user_settings.sh, us = user_settings
    us_file_path = "/scratch2/NCEPDEV/naqfc/Anna.Smoot/git/AnnaSmoot-NOAA/AQM-Workflow/ecf_update/ecf/defs/user_settings.sh"
    # us_process = subprocess.Popen(f'source {us_file_path} && printenv | grep PDY', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    us_process = subprocess.Popen(f'source {us_file_path} && printenv | grep -E "PDY|CYC|RUN|PROJ"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    us_stdout, us_stderr = us_process.communicate()     

    if us_process.returncode !=0:
        raise Exception(f"Error: {us_stderr.decode()}")
    print(f"output: {us_stdout.decode()}")

    #extract user vars
    us_env_vars = {}
    for line in us_stdout.decode().splitlines():
        if "=" in line: 
            key, value = line.split("=", 1)
            us_env_vars[key] = value
    print(f"us_env_vars_out: {us_env_vars}")
    return us_env_vars

'''
#Read in ecflow YAML
with open("testdb.yml" ,'r') as test_yaml:
    try:
        #print yaml contents
        print(yaml.safe_load(test_yaml))
        #load & store but don't print
        #data = yaml.safe_load(test_yaml)
        #print(data)
    except yaml.YAMLError as exc:
        print(exc)
'''

#suite function
def suite(defs):
    suite = defs.add_suite('nco_aqm') 
    print('suite created')
    out_file(defs)

#f_primary, family primary function: 
#This function creates primary family, & calls 2 other functions:
#user settings and machine settings, in order to read & check 
#all ecf.EDITs in the primary family 
def f_primary(defs):
    f_primary = defs.nco_aqm.add_family('primary')
    print('primary family created')
    out_file(defs)

'''
#f_cycle family cycle function: This function checks user_settings.sh
# for number of cycles and sets up cycles 00, 06, 12, or 18
def f_cycle(defs):
    #print cycle we got from user_settings
    if cycle == '00'
        f_00 = defs.nco_aqm.f_primary.add_family('00') #C00?
    elif cycle =='06'
        f_00 = defs.nco_aqm.f_primary.add_family('00') #C00?
        f_06 = defs.nco_aqm.f_primary.add_family('06') #C06?
    elif cycle =='12'
        f_00 = defs.nco_aqm.f_primary.add_family('00') #C00?
        f_06 = defs.nco_aqm.f_primary.add_family('06') #C06?
        f_12 = defs.nco_aqm.f_primary.add_family('12') #C12?
    elif cycle == '18'
        f_00 = defs.nco_aqm.f_primary.add_family('00') #C00?
        f_06 = defs.nco_aqm.f_primary.add_family('06') #C06?
        f_12 = defs.nco_aqm.f_primary.add_family('12') #C12?
        f_18 = defs.nco_aqm.f_primary.add_family('18') #C18?
    else:
        print("Did not enter valid cycle in user_settings.sh. Valid values are: 00, 06, 12, or 18")      
    print(f'cycle families added: {cycle}!')
    out_file(defs)
'''

#This function creates the .def file 
def out_file(defs):
    defs.save_as_defs('./config_test.def')  # save defs into file
    print('test file written')

main()