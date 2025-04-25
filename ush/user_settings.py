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

    #Organization
    try:
        org: str = yaml_us['ORG']
        if org is None:
            print("ERROR: ORG is not set. Set ORG in user_set.yml")
        else:
            print(f"ORG is: {org}")
    except KeyError:
        print("ERROR: Invalid ORG. Set ORG in user_set.yml")

    #queue
    try: 
        queue: str = yaml_us['QUEUE']
        if queue is None:
            print("ERROR: QUEUE is not set. Set QUEUE in user_set.yml")
        else:
            print(f"QUEUE is: {queue}")
    except KeyError:
        print("ERROR: Invalid QUEUE. Set QUEUE in user_set.yml")    

    #workflow mode: realtime or retro
    try: 
        wf_mode: str = yaml_us['workflow_mode']
        if wf_mode is None:
            print("ERROR: workflow_mode is not set. Set workflow_mode in user_set.yml")
        else:
            print(f"aqm_ver is: {wf_mode}")
    except KeyError:
        print("ERROR: Invalid workflow_mode. Set workflow_mode in user_set.yml")

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

    #Read in WCOSS2 only variables:
    if machine_id == 'wcoss2':
        try:
            project: str = yaml_us['PROJ']
            print(f'PROJ is: {project}')
            if project is None:
                print("ERROR: PROJ is not set. Set PROJ in user_set.yml")
            else:
                print(f"PROJ is: {project}")
        except KeyError:
            print("ERROR: Invalid PROJ. Set PROJ in user_set.yml")

        try:
            proj_env: str = yaml_us['PROJENV']
            print(f'PROJENV is: {proj_env}')
            if proj_env is None:
                print("ERROR: PROJENV is not set. Set PROJENV in user_set.yml")
            else:
                print(f"PROJENV is: {proj_env}")
        except KeyError:
            print("ERROR: Invalid PROJENV. Set PROJENV in user_set.yml")

        try:
            net: str = yaml_us['NET']
            print(f'NET is: {net}')
            if net is None:
                print("ERROR: NET is not set. Set NET in user_set.yml")
            else:
                print(f"NET is: {net}")
        except KeyError:
            print("ERROR: Invalid NET. Set NET in user_set.yml")

        try:
            run: str = yaml_us['RUN']
            print(f'RUN is: {run}')
            if run is None:
                print("ERROR: RUN is not set. Set RUN in user_set.yml")
            else:
                print(f"RUN is: {run}")
        except KeyError:
            print("ERROR: Invalid RUN. Set RUN in user_set.yml")

        try:
            envir: str = yaml_us['ENVIR']
            print(f'ENVIR is: {envir}')
            if envir is None:
                print("ERROR: ENVIR is not set. Set ENVIR in user_set.yml")
            else:
                print(f"ENVIR is: {envir}")
        except KeyError:
            print("ERROR: Invalid ENVIR. Set ENVIR in user_set.yml")

        try:
            q_arch: str = yaml_us['QUEUE_ARCH']
            print(f'QUEUE_ARCH is: {q_arch}')
            if q_arch is None:
                print("ERROR: QUEUE_ARCH is not set. Set QUEUE_ARCH in user_set.yml")
            else:
                print(f"QUEUE_ARCH is: {q_arch}")
        except KeyError:
            print("ERROR: Invalid QUEUE_ARCH. Set QUEUE_ARCH in user_set.yml")

        try:
            mach_site: str = yaml_us['MACHINE_SITE']
            print(f'MACHINE_SITE is: {mach_site}')
            if mach_site is None:
                print("ERROR: MACHINE_SITE is not set. Set MACHINE_SITE in user_set.yml")
            else:
                print(f"MACHINE_SITE is: {mach_site}")
        except KeyError:
            print("ERROR: Invalid MACHINE_SITE. Set QMACHINE_SITE in user_set.yml")

    #Type of run: nco, community, or testing
    try:
        run_type: str = yaml_us['RUN_TYPE']
        print(f'run type is: {run_type}')
        if run_type is None:
            print("ERROR: RUN_TYPE is not set. Set RUN_TYPE in user_set.yml")
        else:
            print(f"RUN_TYPE is: {run_type}")
    except KeyError:
        print("ERROR: Invalid RUN_TYPE. Set RUN_TYPE in user_set.yml")

    #Generate ecflow dir, packagehome dir, and output dir
    if machine_id == 'wcoss2':
        try:
            ecf_dir: str = f'/lfs/h2/{org}/{user_group}/noscrub/{user}/ecflow'
            print(f'ecflow directory is: {ecflow_dir}')  
        except Exception as e :
            print(e)
            print(f'ERROR: ecflow directory not genereated!')
        try:
            pack_home: str = f'/lfs/h2/{org}/{user_group}/noscrub/{user}/nwdev/packages/aqm.{aqm_ver}'
            print(f'packagehome is: {pack_home}')  
        except Exception as e :
            print(e)
            print(f'ERROR: packagehome directory not genereated!')
        try:
            out_dir: str = f'/lfs/h2/{org}/ptmp/{user}/ecflow_aqm/para/output/prod/today'
            print(f'output directory is: {out_dir}') 
        except Exception as e :
            print(e)
            print(f'ERROR: output directory directory not genereated!')
    #elif machine_id == 'hera':
    #    
    #else: #assume we're on C6
    #   
     
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
'''

#generate customized ecflow def file
def def_file_generate(defs):
    defs = ecf.Defs()
    #if run_type == 'nco':
    #    suite = defs.add_suite('nco_aqm') #or call aqm_cycled_def.py? 
    #elif run_type == 'testing': 
    #    suite = defs.add_suite('aqm_test') 
    #else:  #assume community (configurable) run
    #    suite = defs.add_suite('aqm_user')
    suite = defs.add_suite('nco_aqm') 
    f_primary = suite.add_family('primary')
    defs.nco_aqm.primary += [ ecf.Edit(aqm_ver = aqm_ver),
                ecf.Edit(PACKAGEHOME = pack_home),
                ecf.Edit(NET = net),
                ecf.Edit(RUN = run),
                ecf.Edit(PROJ = project),
                ecf.Edit(PROJENV = proj_env),
                ecf.Edit(MACHINE_SITE = mach_site),
                ecf.Edit(ENVIR = envir),
                ecf.Edit(QUEUE = queue),
                ecf.Edit(QUEUE_ARCH = q_arch),
                ecf.Edit(OUTPUTDIR = out_dir)] 
    print('Primary family finished!')
    def_file(defs)

#save ecf/defs/output.def
def def_file(defs):
    defs.save_as_defs('../ecf/defs/output.def')
    print('output.def written')

main()
