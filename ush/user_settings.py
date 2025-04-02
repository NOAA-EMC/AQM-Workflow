#This is the user settings script

#imports
import os
import ecflow as ecf
import yaml
import detect_machine
from pathlib import Path

def main():
    yaml_us = yml_read()
    user_set_check(yaml_us)
    def_file_generate()
    def_file()

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
    machine_id: str = detect_machine.get_machine_id()
    print(f'machine_id is: {machine_id}')
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
'''
    #ecf port number
    try:
        ecf_port: int = os.environ['ECF_PORT']
        print(f'ecf_port from ENVIRON: {ecf_port}')
    except KeyError:
        #get user_id & add 1500 to user_id to ge ecf_port
        user_id: int = os.getuid()
        ecf_port: int = user_id + 1500
        print(f'ecf_port from EXCEPTION: {ecf_port}')

    #ECF Host 
    #assumes ecflow is loaded 
        if machine_id == 'wcoss2':
            try:
                ecf_host: str = yaml_us['ECF_HOST']
                print(f"ECF_HOST from YAML: {ecf_host}")
            if None in ecf_host:
                print("KeyError: You are on wcoss2. Please set ECF_HOST in user_set.yml to cdecflow01 or ddecflow01")
                #ecf_host: str = 'cdecflow01'
                #ecf_host: str = 'ddecflow01'
                #if get_host 
        elif machine_id == 'hera':
            try:
                ecf_host: str = yaml_us['ECF_HOST']
                print(f"ECF_HOST from YAML: {ecf_host}")
            if None in ecf_host:
                ecf_host: str = 'hecflow01'
                print(f"ECF_HOST generated: {ecf_host}")
        else:
             try:
                ecf_host: str = yaml_us['ECF_HOST']
                print(f"ECF_HOST from YAML: {ecf_host}")
            if None in ecf_host:
                ecf_host: str = 'gaea66'
                print(f"ECF_HOST generated: {ecf_host}")

    #Location/path for ecflow files
    try:
        ecf_dir: str =  {yaml_us['ecflow_dir']['wcoss2']}
        print(f'ecf_dir from yaml is: {ecflow_dir}')        
    except KeyError:
        if machine_id == 'wcoss2':
            ecf_dir: str = f'/lfs/h2/emc/{user_group}/noscrub/{user}/ecflow'
            print(f'ecf_dir from except is: {ecflow_dir}')  
        #elif machine_id == 'hera':
        #    ecflow_dir: str == ''
        #else: #assume we're on C6
        #    ecflow_dir: str == ''
        #print(f'ecflow_dir from EXCEPTION: {os.environ["ecflow_dir"]}')        

    #Set path to the package
    try: 
        pack_home: str =  {yaml_us['PACKAGEHOME']['wcoss2']}
        print(f'pack_home from yaml is: {pack_home}')  
    except KeyError:
        if machine_id == 'wcoss2':
            pack_home: str = f'/lfs/h2/emc/{user_group}/noscrub/{user}/nwdev/packages/aqm.{aqm_ver}'
            print(f'pack_home from except is: {pack_home}')  
        #elif machine_id == 'hera':
        #    pack_home: str == ''
        #else: #assume we're on C6
        #    pack_home: str == ''

    #Set output directory
    try:
        out_dir: str =  {yaml_us['outputdir']['wcoss2']}
        print(f'out_dir from yaml is: {out_dir}')  

    except KeyError:
        if machine_id == 'wcoss2':
            out_dir: str = f'/lfs/h2/emc/ptmp/{user}/ecflow_aqm/para/output/prod/today'
            print(f'out_dir from except is: {out_dir}')  
        #elif machine_id == 'hera':
        #    outputdir: str == ''
        #else: #assume we're on C6
        #    outputdir: str == ''
'''
#generate customized ecflow def file
def def_file_generate():

#save ecf/defs/output.def
def def_file(defs):
    defs.save_as_defs('../ecf/defs/output.def')
    print('output.def written')

main()
