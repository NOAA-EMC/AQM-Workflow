#This is the user settings script

#imports
import os
import ecflow as ecf
import yaml
import detect_machine
#import subprocess 
from pathlib import Path

#user customizes yaml
#read in and check all user settings

def main():
    #detect_machine()
    yaml_us = yml_read()
    user_set_check(yaml_us)
    #def_file_generate()
    #def_file()

#run detect machine script
#def detect_machine():

#reads in user_set.yml
def yml_read():
        try:
            yaml_us = yaml.safe_load(Path("user_set.yml").read_text())
            print(f" the dict is: {yaml_us}")
            #print(type(yaml_us))
            #print(f"Access hera dir: {yaml_us['user_dir']['hera']}")
            return yaml_us
        except yaml.YAMLError as exc:
            print(exc)

#checks user_set.yaml vars & adds others 
def user_set_check(yaml_us):
    #get username for directory paths
    user: str = os.environ['USER']

    #group to use for workflow
    try:
        user_group: str = yaml_us['USER_GROUP']
        #print(type(user_group))
        #user_group = list(user_group)
        #if None in user_group:
        if user_group is None:
            print("ERROR: USER_GROUP is not set. Set USER_GROUP in user_set.yml")
        else:
            print(f"USER_GROUP is: {user_group}")
    except KeyError:
        print("ERROR: Invalid USER_GROUP. Set USER_GROUP in user_set.yml")

    #version of AQM
    try:
        aqm_ver: str = yaml_us['aqm_ver']
        if aqm_ver is None:
            print("ERROR: aqm_ver is not set. Set aqm_ver in user_set.yml")
        else:
            print(f"aqm_ver is: {aqm_ver}")
    except KeyError:
        print("ERROR: Invalid aqm_ver. Set aqm_ver in user_set.yml")

    #PDY - start date
    try:
        pdy: int = str(yaml_us['PDY']).zfill(8)
        #print(type(pdy))
        if pdy is None:
            print("ERROR: PDY is not set. Set PDY in user_set.yml")
        else:
            print(f"PDY is: {pdy}")
    except KeyError:
        print("ERROR: Invalid PDY. Set PDY in user_set.yml")

    #Workflow mode
    try:
        workflow_mode: str = yaml_us['workflow_mode']
        if workflow_mode is None:
            print("ERROR: workflow_mode is not set. Set workflow_mode in user_set.yml")
        else:
            print(f"workflow_mode is: {workflow_mode}")
    except KeyError:
        print("ERROR: Invalid workflow_mode. Set workflow_mode in user_set.yml")

    #Cycles (00, 06, 12, or 18)
    try:
        cyc: int = str(yaml_us['CYC']).zfill(2)
        if cyc is None:
            print("ERROR: CYC is not set. Set CYC in user_set.yml")
        else:
            print(f"CYC is: {cyc}")
    except KeyError:
        print("ERROR: Invalid CYC. Set CYC in user_set.yml")

    #Check the machine_id from detect_machine.sh and use it to get user_dir from user_set.yml
    #machine_id: str = os.environ.get('MACHINE_ID')
    machine_id: str = detect_machine.get_machine_id()
    print(f'machine_id is: {machine_id}')
    #print(type(machine_id))
    #print(f"user_dir: {yaml_us['user_dir']['hera']}")
    if machine_id == 'wcoss2':
        try:
            user_dir: str =  {yaml_us['user_dir']['wcoss2']}
            print(f'From try, user_dir is: {user_dir}')
            if None in user_dir:
                raise KeyError("ERROR: USER_DIR is not set. Set USER_DIR in user_set.yml")
        except Exception as e :
            print(e)
            cwd = os.getcwd()
            user_dir: str = cwd
            print(f'From except, user_dir is: {user_dir}')
    elif machine_id == 'hera':
        try:
            user_dir: str =  {yaml_us['user_dir']['hera']}
            print(f'From try, user_dir is: {user_dir}')
            if None in user_dir:
                raise KeyError("ERROR: USER_DIR is not set. Set USER_DIR in user_set.yml")
        except Exception as e :
            print(e)
            cwd = os.getcwd()
            user_dir: str = cwd
            print(f'From except, user_dir is: {user_dir}')
    else:
        try:
            user_dir: str =  {yaml_us['user_dir']['gaeac6']}
            print(f'From try, user_dir is: {user_dir}')
            if None in user_dir:
                raise KeyError("ERROR: USER_DIR is not set. Set USER_DIR in user_set.yml")
        except Exception as e :
            print(e)
            cwd = os.getcwd()
            user_dir: str = cwd
            print(f'From except, user_dir is: {user_dir}')

    #ECFlow Host Server Location
    #Before running this script, in the command line enter "module load ecflow"
    #This can be left blank if set by module load properly


'''
    #ECFlow Host Server Location
    #Before running this script, in the command line enter "module load ecflow"
    #This can be left blank if set by module load properly
    try:
        ecf_host: str = os.environ.get('ECF_HOST')
        #os.environ['ECF_HOST'] = ecf_host
        #print(f'ecf_host from ENVIRON: {os.environ["ECF_HOST"]}')
    except KeyError:
        machine_id: str = os.environ.get('MACHINE_ID')
        #os.environ['MACHINE_ID'] = machine_id
        print(f'machine_id from EXCEPTION: {machine_id}')
        if machine_id == 'cactus':
            ecf_host: str = 'cdecflow01'
            os.environ['ECF_HOST'] = ecf_host
        elif machine_id == 'dogwood':
            ecf_host: str = 'ddecflow01'
            os.environ['ECF_HOST'] = ecf_host
        elif machine_id == 'hera':
            ecf_host: str = 'hecflow01'
            os.environ['ECF_HOST'] = ecf_host
        else:
            ecf_host: str = 'gaea66'
            os.environ['ECF_HOST'] = ecf_host
        #print(f'ecf_host from EXCEPTION: {os.environ["ECF_HOST"]}')

    #ecf port number
    #Before running this script, in the command line enter "module load ecflow"
    #This can be left blank if set by module load properly
    try:
        ecf_port: int = os.environ['ECF_PORT']
        #print(f'ecf_port from ENVIRON: {os.environ["ECF_PORT"]}')
    except KeyError:
        #get user_id & add 1500 to user_id to ge ecf_port
        user_id: int = os.getuid()
        #print(f'user_id is from EXCEPTION: {user_id}')
        ecf_port: int = user_id + 1500
        #print(f'ecf_port from EXCEPTION: {os.environ["ECF_PORT"]}')

    #Location/path for ecflow files
    #No need to edit this
    try:
        ecflow_dir: str = f'/lfs/h2/emc/{os.environ["user_group"]}/noscrub/{os.environ["USER"]}/ecflow'
        os.environ['ecflow_dir'] = ecflow_dir
        #print(f'ecf_dir is: {os.environ["ecflow_dir"]}')
    except KeyError:
        if machine_id == 'cactus':
            ecflow_dir: str = f'/lfs/h2/emc/{os.environ["user_group"]}/noscrub/{os.environ["USER"]}/ecflow'
            os.environ['ecflow_dir'] = ecflow_dir
        elif machine_id == 'dogwood':
            ecflow_dir: str = f'/lfs/h2/emc/{os.environ["user_group"]}/noscrub/{os.environ["USER"]}/ecflow'
            os.environ['ecflow_dir'] = ecflow_dir
        #elif machine_id == 'hera':
        #    ecflow_dir: str == ''
        #    os.environ['ecflow_dir'] = ecflow_dir
        #else: #assume we're on C6
        #    ecflow_dir: str == ''
        #    os.environ['ecflow_dir'] = ecflow_dir
        #print(f'ecflow_dir from EXCEPTION: {os.environ["ecflow_dir"]}')        

    #Set path to the package
    #The user should not need to edit this
    #Package on WCOSS2
    try: 
        packagehome: str = f'/lfs/h2/emc/physics/noscrub/{os.environ["USER"]}/nwdev/packages/aqm.{os.environ["aqm_ver"]}'
        os.environ['PACKAGEHOME'] = packagehome
        #print(f'package home is: {os.environ["PACKAGEHOME"]}')
    except KeyError:
        if machine_id == 'cactus':
            packagehome: str = f'/lfs/h2/emc/physics/noscrub/{os.environ["USER"]}/nwdev/packages/aqm.{os.environ["aqm_ver"]}'
            os.environ['PACKAGEHOME'] = packagehome
        elif machine_id == 'dogwood':
            packagehome: str = f'/lfs/h2/emc/physics/noscrub/{os.environ["USER"]}/nwdev/packages/aqm.{os.environ["aqm_ver"]}'
            os.environ['PACKAGEHOME'] = packagehome
        #elif machine_id == 'hera':
        #    packagehome: str == ''
        #    os.environ['PACKAGEHOME'] = packagehome
        #else: #assume we're on C6
        #    packagehome: str == ''
        #    os.environ['PACKAGEHOME'] = packagehome
        #print(f'packagehome from EXCEPTION: {os.environ["PACKAGEHOME"]}')

    #Set output directory
    #The user should not need to edit this 
    try:
        outputdir: str = f'/lfs/h2/emc/ptmp/{os.environ["USER"]}/ecflow_aqm/para/output/prod/today'
        os.environ['OUTPUTDIR']= outputdir
        #print(f'output dir is: {os.environ["OUTPUTDIR"]}')
    except KeyError:
        if machine_id == 'cactus':
            outputdir: str = f'/lfs/h2/emc/ptmp/{os.environ["USER"]}/ecflow_aqm/para/output/prod/today'
            os.environ['OUTPUTDIR'] = outputdir
        elif machine_id == 'dogwood':
            outputdir: str = f'/lfs/h2/emc/ptmp/{os.environ["USER"]}/ecflow_aqm/para/output/prod/today'
            os.environ['OUTPUTDIR'] = outputdir
        #elif machine_id == 'hera':
        #    outputdir: str == ''
        #    os.environ['OUTPUTDIR'] = outputdir
        #else: #assume we're on C6
        #    outputdir: str == ''
        #    os.environ['OUTPUTDIR'] = outputdir
        #print(f'outputdir from EXCEPTION: {os.environ["OUTPUTDIR"]}')

#generate customized ecflow def file
def def_file_generate():
 
def def_file(defs):
    defs.save_as_defs('./def_out.def')  # save defs into file
    print('def_out.def written')
'''
main()
