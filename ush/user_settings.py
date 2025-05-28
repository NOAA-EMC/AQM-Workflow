"""
This script takes in user setting vars from user_set.yml in /ush, 
checks them, then generates the ecflow.def file in /ecf/defs
"""

#imports
import os
import subprocess
import ecflow as ecf
import yaml
import detect_machine
from pathlib import Path

def main():
    yaml_us = yml_read()
    vars_dict = {}
    user_set_check(yaml_us, vars_dict)
    defs=ecf.Defs
    def_file_generate(defs, vars_dict)
    def_file(defs)

#reads in user_set.yml
def yml_read():
    """Reads in user_set.yml file"""
    try:
        yaml_us = yaml.safe_load(Path("user_set.yml").read_text())
        print(f" the dict is: {yaml_us}")
        return yaml_us
    except yaml.YAMLError as exc:
        print(exc)

#checks user_set.yaml vars & adds others 
def user_set_check(yaml_us, vars_dict):
    """
    Check vars set in user_set.yml and returns errors
    for incorrect or unset vars.
    Saves checked vars to dictionary: vars_dict.
    """
    #get username for directory paths
    user: str = os.environ['USER']
    vars_dict['user'] = user

    #group to use for workflow
    try:
        user_group: str = yaml_us['USER_GROUP']
        if user_group is None:
            raise TypeError("ERROR: USER_GROUP is not set. Set USER_GROUP in user_set.yml")
        else:
            print(f"USER_GROUP is: {user_group}")
            vars_dict['user_group'] = user_group
    except:
        raise KeyError("ERROR:Invalid USER_GROUP. Set USER_GROUP in user_set.yml")

    #version of AQM
    try:
        AQM_version: str = yaml_us['aqm_ver']
        vars_dict['aqm_ver'] = AQM_version
        if AQM_version is None:
            raise TypeError("ERROR: aqm_ver is not set. Set aqm_ver in user_set.yml")
        else:
            print(f"aqm_ver is: {AQM_version}")
            vars_dict['aqm_ver'] = AQM_version
    except:
        raise KeyError("ERROR: Invalid aqm_ver. Set aqm_ver in user_set.yml")

    #Organization
    try:
        org: str = yaml_us['ORG']
        if org is None:
            raise TypeError("ERROR: ORG is not set. Set ORG in user_set.yml")
        else:
            print(f"ORG is: {org}")
            vars_dict['org'] = org
    except:
        raise KeyError("ERROR: Invalid ORG. Set ORG in user_set.yml")

    #queue
    try: 
        queue: str = yaml_us['QUEUE']
        if queue is None:
            raise TypeError("ERROR: QUEUE is not set. Set QUEUE in user_set.yml")
        else:
            print(f"QUEUE is: {queue}")
            vars_dict['QUEUE'] = queue
    except:
        raise KeyError("ERROR: Invalid QUEUE. Set QUEUE in user_set.yml")   

    #PDY - start date
    try:
        pdy: int = str(yaml_us['PDY']).zfill(8)
        if pdy is None:
            raise TypeError("ERROR: PDY is not set. Set PDY in user_set.yml")
        else:
            print(f"PDY is: {pdy}")
            vars_dict['pdy'] = pdy
    except:
        raise KeyError("ERROR: Invalid PDY. Set PDY in user_set.yml")        

    #workflow mode: realtime or retro
    try: 
        wf_mode: str = yaml_us['workflow_mode']
        if wf_mode is None:
            raise TypeError("ERROR: workflow_mode is not set. Set workflow_mode in user_set.yml")
        else:
            print(f"workflow_mode is: {wf_mode}")
            vars_dict['workflow_mode'] = wf_mode
    except:
        raise KeyError("ERROR: Invalid workflow_mode. Set workflow_mode in user_set.yml")

    #Cycles (00, 06, 12, or 18)
    try:
        cyc: int = yaml_us['CYC']
        print(type(cyc))
        if cyc is None:
            raise TypeError("ERROR: CYC is not set. Set CYC in user_set.yml")
        else:
            print(f"CYC is: {cyc}")
            vars_dict['cycle'] = cyc
    except:
        raise KeyError("ERROR: Invalid CYC. Set CYC in user_set.yml")

    #Check the machine_id from detect_machine.sh and use it to get user_dir from user_set.yml
    machine_id: str = detect_machine.get_machine_id()
    #print(f'machine_id is: {machine_id}')
    if machine_id == 'wcoss2':
        try:
            user_dir: str =  yaml_us['user_dir']['wcoss2']
            print(f'From try, user_dir is: {user_dir}')
            vars_dict['user_dir'] = user_dir
        except Exception as e:
            print(e)
            cwd = os.getcwd()
            user_dir: str = cwd
            print(f'From except, user_dir is: {user_dir}')
            vars_dict['user_dir'] = user_dir
    elif machine_id == 'hera':
        try:
            user_dir: str =  yaml_us['user_dir']['hera']
            print(f'From try, user_dir is: {user_dir}')
            vars_dict['user_dir'] = user_dir
        except Exception as e:
            print(e)
            cwd = os.getcwd()
            user_dir: str = cwd
            print(f'From except, user_dir is: {user_dir}')
            vars_dict['user_dir'] = user_dir
    else:
        try:
            user_dir: str =  yaml_us['user_dir']['gaeac6']
            print(f'From try, user_dir is: {user_dir}')
            vars_dict['user_dir'] = user_dir
        except Exception as e:
            print(e)
            cwd = os.getcwd()
            user_dir: str = cwd
            print(f'From except, user_dir is: {user_dir}')
            vars_dict['user_dir'] = user_dir

#ecf.edits core vars
    try:
        project: str = yaml_us['PROJ']
        print(f'PROJ is: {project}')
        vars_dict['PROJ'] = project
        if project is None:
            raise TypeError("ERROR: PROJ is not set. Set PROJ in user_set.yml")
    except:
        raise KeyError("ERROR: Invalid PROJ. Set PROJ in user_set.yml")

    try:
        proj_env: str = yaml_us['PROJENV']
        print(f'PROJENV is: {proj_env}')
        vars_dict['PROJENV'] = proj_env
        if proj_env is None:
            raise TypeError("ERROR: PROJENV is not set. Set PROJENV in user_set.yml")
    except:
        raise KeyError("ERROR: Invalid PROJENV. Set PROJENV in user_set.yml")

    try:
        net: str = yaml_us['NET']
        print(f'NET is: {net}')
        vars_dict['NET'] = net
        if net is None:
            raise TypeError("ERROR: NET is not set. Set NET in user_set.yml")
    except:
        raise KeyError("ERROR: Invalid NET. Set NET in user_set.yml")            

    try:
        run: str = yaml_us['RUN']
        print(f'RUN is: {run}')
        vars_dict['RUN'] = run
        if run is None:
            raise TypeError("ERROR: RUN is not set. Set RUN in user_set.yml")
    except:
        raise KeyError("ERROR: Invalid RUN. Set RUN in user_set.yml")

    try:
        envir: str = yaml_us['ENVIR']
        print(f'ENVIR is: {envir}')
        vars_dict['ENVIR'] = envir
        if envir is None:
            raise TypeError("ERROR: ENVIR is not set. Set ENVIR in user_set.yml")
    except:
        raise KeyError("ERROR: Invalid ENVIR. Set ENVIR in user_set.yml")

    try:
        q_arch: str = yaml_us['QUEUE_ARCH']
        print(f'QUEUE_ARCH is: {q_arch}')
        vars_dict['QUEUE_ARCH'] = q_arch
        if q_arch is None:
            raise TypeError("ERROR: QUEUE_ARCH is not set. Set QUEUE_ARCH in user_set.yml")
    except:
        raise KeyError("ERROR: Invalid QUEUE_ARCH. Set QUEUE_ARCH in user_set.yml")

    try:
        mach_site: str = yaml_us['MACHINE_SITE']
        print(f'MACHINE_SITE is: {mach_site}')
        vars_dict['MACHINE_SITE'] = mach_site
        if mach_site is None:
            raise TypeError("ERROR: MACHINE_SITE is not set. Set MACHINE_SITE in user_set.yml")
    except:
        raise KeyError("ERROR: Invalid MACHINE_SITE. Set QMACHINE_SITE in user_set.yml")

    #Type of run: nco, community, or testing
    try:
        run_type: str = yaml_us['RUN_TYPE']
        print(f'run type is: {run_type}')
        vars_dict['run_type'] = run_type
        if run_type is None:
            raise TypeError("ERROR: RUN_TYPE is not set. Set RUN_TYPE in user_set.yml")
    except:
        raise KeyError("ERROR: Invalid RUN_TYPE. Set RUN_TYPE in user_set.yml")

    #Generate ecflow dir, packagehome dir, ECF_INCLUDE, and output dir
    if machine_id == 'wcoss2':
        try:
            ecf_dir: str = f'/lfs/h2/{org}/{user_group}/noscrub/{user}/ecflow'
            print(f'ecflow directory is: {ecflow_dir}')
            vars_dict['ecf_dir'] = ecf_dir  
        except Exception as e:
            print(e)
            raise KeyError("ERROR: ecflow directory not genereated!")
        try:
            pack_home: str = f'/lfs/h2/{org}/{user_group}/noscrub/{user}/nwdev/packages/aqm.{AQM_version}'
            ecf_files: str = f'{pack_home}/ecf'
            print(f'packagehome is: {pack_home}')
            print(f'ecf_files is: {ecf_files}')
            vars_dict['PACKAGEHOME'] = pack_home
            vars_dict['ECF_FILES'] = ecf_files  
        except Exception as e:
            print(e)
            raise KeyError("ERROR: packagehome not genereated!")
        try:
            out_dir: str = f'/lfs/h2/{org}/ptmp/{user}/ecflow_aqm/para/output/prod/today'
            print(f'output directory is: {out_dir}')
            vars_dict['OUTPUTDIR'] = out_dir 
        except Exception as e:
            print(e)
            raise KeyError("ERROR: output directory not genereated!")
    elif machine_id == 'hera':
        try:
            ecf_dir: str = f'/scratch2/{org}/{user_group}/{user}'
            print(f'ecflow directory is: {ecf_dir}')
            vars_dict['ecf_dir'] = ecf_dir  
        except Exception as e:
            print(e)
            raise KeyError("ERROR: ecflow directory not genereated!")
        try:
            pack_home: str = f'/scratch2/{org}/{user_group}/{user}/nwdev/packages/aqm.{AQM_version}'
            ecf_files: str = f'{pack_home}/ecf'
            print(f'packagehome is: {pack_home}')
            print(f'ecf_files is: {ecf_files}')
            vars_dict['PACKAGEHOME'] = pack_home
            vars_dict['ECF_FILES'] = ecf_files  
        except Exception as e:
            print(e)
            raise KeyError("ERROR: packagehome not genereated!")
        try:
            out_dir: str = f'/scratch2/{org}/{user}/ecflow_aqm/para/output/prod/today'
            print(f'output directory is: {out_dir}')
            vars_dict['OUTPUTDIR'] = out_dir 
        except Exception as e:
            print(e)
            raise KeyError("ERROR: output directory not genereated!")
    else: #assume Gaea C6
        try:
            ecf_dir: str = f'/gpfs/f6/{project}/scratch/{user}/noscrub/{user}/ecflow'
            print(f'ecflow directory is: {ecflow_dir}')
            vars_dict['ecf_dir'] = ecf_dir  
        except Exception as e:
            print(e)
            raise KeyError("ERROR: ecflow directory not genereated!")
        try:
            pack_home: str = f'/gpfs/f6/{project}/world-shared/{user}/nwdev/packages/aqm.{AQM_version}'
            ecf_files: str = f'{pack_home}/ecf'
            print(f'packagehome is: {pack_home}')
            print(f'ecf_files is: {ecf_files}')
            vars_dict['PACKAGEHOME'] = pack_home
            vars_dict['ECF_FILES'] = ecf_files  
        except Exception as e:
            print(e)
            raise KeyError("ERROR: packagehome not genereated!")
        try:
            out_dir: str = f'/gpfs/f6/{project}/scratch/{user}/ecflow_aqm/para/output/prod/today'
            print(f'output directory is: {out_dir}')
            vars_dict['OUTPUTDIR'] = out_dir 
        except Exception as e:
            print(e)
            raise KeyError("ERROR: output directory not genereated!")

    #Get ecf_include from setup_ecflow.sh
    #set_ecflow_path = pack_home #try to get it without running it 
    set_ecflow_path = '/scratch2/NCEPDEV/naqfc/Anna.Smoot/git/AnnaSmoot-NOAA/AQM-Workflow/ecf_update/ush/setup_ecflow.sh'
    #set_ecflow_path = f'{pack_home}/ush/setup_ecflow.sh'
    set_ecflow_process = subprocess.Popen(f'source {set_ecflow_path} && printenv | grep -E "ECF_INCLUDE"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    set_ecflow_stdout, set_ecflow_stderr = set_ecflow_process.communicate()

    if set_ecflow_process.returncode != 0:
        raise KeyError(f"Error: {set_ecflow_stderr.decode()}")
        print(f"output: {set_ecflow_stdout.decode()}")

    for line in set_ecflow_stdout.decode().splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            vars_dict['ECF_INCLUDE'] = value
            print(vars_dict['ECF_INCLUDE'])

    return vars_dict
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
def def_file_generate(defs, vars_dict):
    """Generate the ecflow.def file based on user_set.yml"""
    defs = ecf.Defs()
    #print(f"From def file gen func: {vars_dict}")
    if vars_dict['run_type'] == 'nco':
        suite = defs.add_suite('nco_aqm') #or call aqm_cycled_def.py? 
        f_primary = suite.add_family('primary')
        defs.nco_aqm.primary += [ #ecf.Edit(aqm_ver = vars_dict['aqm_ver']),
            ecf.Edit(PACKAGEHOME = vars_dict['PACKAGEHOME']),
            ecf.Edit(NET = vars_dict['NET']),
            ecf.Edit(RUN = vars_dict['RUN']),
            ecf.Edit(PROJ = vars_dict['PROJ']),
            ecf.Edit(PROJENV = vars_dict['PROJENV']),
            ecf.Edit(MACHINE_SITE = vars_dict['MACHINE_SITE']),
            ecf.Edit(ENVIR = vars_dict['ENVIR']),
            ecf.Edit(QUEUE = vars_dict['QUEUE']),
            ecf.Edit(QUEUE_ARCH = vars_dict['QUEUE_ARCH']),
            ecf.Edit(OUTPUTDIR = vars_dict['OUTPUTDIR']),
            ecf.Edit(ECF_INCLUDE = vars_dict['ECF_INCLUDE'])]


    elif vars_dict['run_type'] == 'testing':
        suite = defs.add_suite('aqm_test') 
        f_primary = suite.add_family('primary')
        defs.aqm_test.primary += [ #ecf.Edit(aqm_ver = vars_dict['aqm_ver']),
            ecf.Edit(PACKAGEHOME = vars_dict['PACKAGEHOME']),
            ecf.Edit(NET = vars_dict['NET']),
            ecf.Edit(RUN = vars_dict['RUN']),
            ecf.Edit(PROJ = vars_dict['PROJ']),
            ecf.Edit(PROJENV = vars_dict['PROJENV']),
            ecf.Edit(MACHINE_SITE = vars_dict['MACHINE_SITE']),
            ecf.Edit(ENVIR = vars_dict['ENVIR']),
            ecf.Edit(QUEUE = vars_dict['QUEUE']),
            ecf.Edit(QUEUE_ARCH = vars_dict['QUEUE_ARCH']),
            ecf.Edit(OUTPUTDIR = vars_dict['OUTPUTDIR']),
            ecf.Edit(ECF_INCLUDE = vars_dict['ECF_INCLUDE'])]
        #cyc: int = str(yaml_us['CYC']).zfill(2)
        cyc_list = vars_dict['cycle']
        print(f'cyc_list type is: {type(cyc_list)}')
        print(f'cyc_list is: {cyc_list}') 
         
        #print(f' Cycle lenght is: {len(cyc_list)}')
        #for i in range(len(cyc_list)):
        #    if i == "'":
        #         cyc_list[i] = cyc_list.strip("'")
        #print(f'new cyc_list is: {cyc_list}')
        
    else:  #assume community (configurable) run
        suite = defs.add_suite('aqm_user')
        f_primary = suite.add_family('primary')
        defs.aqm_user.primary += [ #ecf.Edit(aqm_ver = vars_dict['aqm_ver']),
            ecf.Edit(PACKAGEHOME = vars_dict['PACKAGEHOME']),
            ecf.Edit(NET = vars_dict['NET']),
            ecf.Edit(RUN = vars_dict['RUN']),
            ecf.Edit(PROJ = vars_dict['PROJ']),
            ecf.Edit(PROJENV = vars_dict['PROJENV']),
            ecf.Edit(MACHINE_SITE = vars_dict['MACHINE_SITE']),
            ecf.Edit(ENVIR = vars_dict['ENVIR']),
            ecf.Edit(QUEUE = vars_dict['QUEUE']),
            ecf.Edit(QUEUE_ARCH = vars_dict['QUEUE_ARCH']),
            ecf.Edit(OUTPUTDIR = vars_dict['OUTPUTDIR']),
            ecf.Edit(ECF_INCLUDE = vars_dict['ECF_INCLUDE'])]

    print('Primary family finished!')
    def_file(defs)

#save ecf/defs/output.def
def def_file(defs):
    try:
        defs.save_as_defs('../ecf/defs/output.def')
        print('output.def written')
    except Exception:
        print('Caught Error')


main()
