
"""
This script checks user_settings.sh for run_type.
It then reads in and checks variables from the appropriate
run_type based yaml: nco_aqm.yml, user_aqm.yml, or test_aqm.yml
It then generates the ecflow.def file in /ecf/defs
"""

#imports
import os
import subprocess
import ecflow as ecf
import yaml
import detect_machine
from pathlib import Path

def main():
    #create empty dictionary
    vars_dict = {}
    user_set_check(vars_dict)
    defs=ecf.Defs
    def_file_generate(defs, vars_dict)
    def_file(defs)

#checks user_set.yaml vars & adds others 
def user_set_check(vars_dict):
    """
    user_set_check() performs 3 tasks:
    1. Read in the run type set in user_settings.sh.
    The run type determines which yaml is read in: 
    test_aqm.yml, nco_aqm.yml, or user_aqm.yml. 
    2. Read in the yaml variables
    3. Perform sanity/error checks on varibles 
    3. Save the checked variables to dictionary: vars_dict.
    The dictionary is then passed to def_file_fenerate()
    """
    #get username for directory paths from environment
    user: str = os.environ['USER']
    #add user name to the dictionary
    vars_dict['user'] = user
    print(vars_dict['user'])

    #The path to user_settings.sh should be in /ush, the same directoary as this script
    user_set_path = './user_settings.sh'
    #Source the user_settings.sh and get run_type variable
    user_set_process = subprocess.Popen(f'source {user_set_path} && printenv | grep -E "run_type"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    user_set_stdout, user_set_stderr = user_set_process.communicate()
    #Check for errors in retrieving the run_type variable 
    if user_set_process.returncode != 0:
        raise KeyError(f"Error: {user_set_stderr.decode()}")
        print(f"output: {user_set_stdout.decode()}")
    #Add the run type to the dictionary
    for line in user_set_stdout.decode().splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            vars_dict['RUN_TYPE'] = value
            print(f'Selected run type from user_settings.sh is:')
            print(vars_dict['RUN_TYPE'])
    
    #read correct yaml (test_aqm.yml, nco_aqm.yml, or user_aqm.yml) based on run type (test, nco, or user)
    #try to load nco_aqm.yml
    if vars_dict['RUN_TYPE'] == 'nco':
        try:
            yaml_us = yaml.safe_load(Path("nco_aqm.yml").read_text())
            print(f"from nco_aqm.yml, yml is: {yaml_us}")
        #otherwise display error
        except yaml.YAMLError as exc:
            print(exc)
    #try to load test_aqm.yml
    elif vars_dict['RUN_TYPE'] == 'test':
        try:
            yaml_us = yaml.safe_load(Path("test_aqm.yml").read_text())
            print(f"from test_aqm.yml, yaml is: {yaml_us}")
        #otherwise display error
        except yaml.YAMLError as exc:
            print(exc)
    #try to load user_aqm.yml
    elif vars_dict['RUN_TYPE'] == 'user':
        try:
            yaml_us = yaml.safe_load(Path("user_aqm.yml").read_text())
            print(f"from user_aqm.yml, yaml is: {yaml_us}")
        #otherwise display error
        except yaml.YAMLError as exc:
            print(exc)

    #try to read user group from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    try:
        user_group: str = yaml_us['USER_GROUP']
        print(f'User group is: {user_group}')
        #check for unacceptable NoneType
        if user_group is None:
            raise TypeError("ERROR: USER_GROUP is not set. Set USER_GROUP in yaml")
        #if type is ok, add to dictionary
        else:
            vars_dict['user_group'] = user_group
    #if there is no USER_GROUP set in yaml, raise KeyError
    except:
        raise KeyError("ERROR:Invalid USER_GROUP. Set USER_GROUP in yaml")

    #try to read the version of AQM from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    try:
        AQM_version: str = yaml_us['aqm_ver']
        vars_dict['aqm_ver'] = AQM_version
        #check for unacceptable NoneType
        if AQM_version is None:
            raise TypeError("ERROR: aqm_ver is not set. Set aqm_ver in yaml")
        #if type is ok, add to dictionary
        else:
            vars_dict['aqm_ver'] = AQM_version
    #if there is no aqm_ver set in yaml, raise KeyError
    except:
        raise KeyError("ERROR: Invalid aqm_ver. Set aqm_ver in yaml")

    #try to read organization from from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    try:
        org: str = yaml_us['ORG']
        print(f'org is: {org}')
        #check for unacceptable NoneType
        if org is None:
            raise TypeError("ERROR: ORG is not set. Set ORG in yaml")
        #if type is ok, add to dictionary
        else:
            vars_dict['org'] = org
    #if there is no ORG set in yaml, raise KeyError
    except:
        raise KeyError("ERROR: Invalid ORG. Set ORG in yaml")

    #try to read queue from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    try: 
        queue: str = yaml_us['QUEUE']
        #check for unacceptable NoneType
        if queue is None:
            raise TypeError("ERROR: QUEUE is not set. Set QUEUE in yaml")
        #if type is ok, add to dictionary
        else:
            vars_dict['QUEUE'] = queue
    #if there is no QUEUE set in yaml, raise KeyError
    except:
        raise KeyError("ERROR: Invalid QUEUE. Set QUEUE in yaml")   

    #try to read PDY (start date) from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    try:
        pdy: int = str(yaml_us['PDY']).zfill(8)
        #check for unacceptable NoneType
        if pdy is None:
            raise TypeError("ERROR: PDY is not set. Set PDY in yaml")
        #if type is ok, add to dictionary
        else:
            vars_dict['pdy'] = pdy
    #if there is no QUEUE set in yaml, raise KeyError
    except:
        raise KeyError("ERROR: Invalid PDY. Set PDY in yaml")

    #Try to read restart frequency variable from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    #and add it to the dictionary   
    try:
        restart_freq: int = yaml_us['RESTART_FREQ']
        vars_dict['RESTART_FREQ'] = restart_freq
    #if there is no RESTART_FREQ set in yaml, raise KeyError
    except:
        raise KeyError("ERROR: Invalid RESTART_FREQ. Set RESTART_FREQ in yaml")

    #Try to read cycle var from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    #and add it to the dictionary   
    try:
        cyc: int = yaml_us['CYC']
        vars_dict['CYC'] = cyc
    #if there is no CYC set in yaml, raise KeyError
    except:
        raise KeyError("ERROR: Invalid CYC. Set CYC in yaml")

    #Try to read forecast hours variable from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    try:
        fcst_hr: int = yaml_us['HOURS']
        #check that cycle & forecast hours arrays are the same length
        fcst_len = len(cyc)
        cyc_len = len(fcst_hr)
        #if arrays are not the same length generate ValueError
        if len(cyc) != len(fcst_hr): 
            raise ValueError("ERROR: forecast hours & cycle array lengths must match. Check HOURS and CYC in yaml")
        #if arrays are the same length, add forecast hours to the dictionary
        else:
            vars_dict['HOURS'] = fcst_hr
    #if there is no HOURS set in yaml, raise KeyError
    except:
        raise KeyError("ERROR: Invalid forecast hours. Set HOURS in yaml")

    #Try to read project variable from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    #and add it to the dictionary
    try:
        project: str = yaml_us['PROJ']
        vars_dict['PROJ'] = project
        #check for unacceptable NoneType
        if project is None:
            raise TypeError("ERROR: PROJ is not set. Set PROJ in yaml")
    #if there is no PROJ set in yaml, raise KeyError
    except:
        raise KeyError("ERROR: Invalid PROJ. Set PROJ in yaml")

    #Try to read project environment variable from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    #and add it to the dictionary
    try:
        proj_env: str = yaml_us['PROJENVIR']
        vars_dict['PROJENVIR'] = proj_env
        #check for unacceptable NoneType
        if proj_env is None:
            raise TypeError("ERROR: PROJENVIR is not set. Set PROJENVIR in yaml")
    #if there is no PROJENVIR set in yaml, raise KeyError
    except:
        raise KeyError("ERROR: Invalid PROJENVIR. Set PROJENVIR in yaml")

    #Try to read net variable from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    #and add it to the dictionary
    try:
        net: str = yaml_us['NET']
        vars_dict['NET'] = net
        #check for unacceptable NoneType
        if net is None:
            raise TypeError("ERROR: NET is not set. Set NET in yaml")
    #if there is no NET set in yaml, raise KeyError
    except:
        raise KeyError("ERROR: Invalid NET. Set NET in yaml")            

    #Run var from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    #and add it to the dictionary
    try:
        run: str = yaml_us['RUN']
        vars_dict['RUN'] = run
        #check for unacceptable NoneType
        if run is None:
            raise TypeError("ERROR: RUN is not set. Set RUN in yaml")
    #if there is no RUN set in yaml, raise KeyError
    except:
        raise KeyError("ERROR: Invalid RUN. Set RUN in yaml")

    #Try to read environment variable from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    #and add it to the dictionary
    try:
        envir: str = yaml_us['ENVIR']
        vars_dict['ENVIR'] = envir
        #check for unacceptable NoneType
        if envir is None:
            raise TypeError("ERROR: ENVIR is not set. Set ENVIR in yaml")
    #if there is no ENVIR set in yaml, raise KeyError
    except:
        raise KeyError("ERROR: Invalid ENVIR. Set ENVIR in yaml")

    #Try to read queue arch variable from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    #and add it to the dictionary
    try:
        q_arch: str = yaml_us['QUEUE_ARCH']
        vars_dict['QUEUE_ARCH'] = q_arch
        #check for unacceptable NoneType
        if q_arch is None:
            raise TypeError("ERROR: QUEUE_ARCH is not set. Set QUEUE_ARCH in yaml")
    #if there is no QUEUE_ARCH set in yaml, raise KeyError
    except:
        raise KeyError("ERROR: Invalid QUEUE_ARCH. Set QUEUE_ARCH in yaml")

    #Try to read machine site variable from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    #and add it to the dictionary
    try:
        mach_site: str = yaml_us['MACHINE_SITE']
        vars_dict['MACHINE_SITE'] = mach_site
        #check for unacceptable NoneType
        if mach_site is None:
            raise TypeError("ERROR: MACHINE_SITE is not set. Set MACHINE_SITE in yaml")
    #if there is no MACHINE_SITE set in yaml, raise KeyError
    except:
        raise KeyError("ERROR: Invalid MACHINE_SITE. Set QMACHINE_SITE in yaml")

    #Try to read workflow mode variable from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    #and add it to the dictionary
    try: 
        wf_mode: str = yaml_us['MODE']
        #check for unacceptable NoneType
        if wf_mode is None:
            raise TypeError("ERROR: workflow_mode is not set. Set workflow_mode in yaml")
        else:
            vars_dict['workflow_mode'] = wf_mode
    #if there is no MODE set in yaml, raise KeyError
    except:
        raise KeyError("ERROR: Invalid workflow_mode. Set workflow_mode in yaml")

    #Check the machine_id from detect_machine.sh (see imports) 
    machine_id: str = detect_machine.get_machine_id()
    if machine_id == 'wcoss2':
        #Try and use machine_id to get user the user directory from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
        #and add it to the dictionary
        try:
            user_dir: str =  yaml_us['user_dir']['wcoss2']
            print(f'From try, user_dir is: {user_dir}')
            vars_dict['user_dir'] = user_dir
        #if user_dir not found in yaml, use cwd
        except Exception as e:
            print(e)
            cwd = os.getcwd()
            user_dir: str = cwd
            print(f'From except, user_dir is: {user_dir}')
            vars_dict['user_dir'] = user_dir
        #Try and use machine_id to get user the user directory from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
        #and add it to the dictionary
    elif machine_id == 'hera':
        try:
            user_dir: str =  yaml_us['user_dir']['hera']
            print(f'From try, user_dir is: {user_dir}')
            vars_dict['user_dir'] = user_dir
        #if user_dir not found in yaml, use cwd
        except Exception as e:
            print(e)
            cwd = os.getcwd()
            user_dir: str = cwd
            print(f'From except, user_dir is: {user_dir}')
            vars_dict['user_dir'] = user_dir
        #Try and use machine_id to get user the user directory from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
        #and add it to the dictionary
    elif machine_id == 'gaeac6':
        try:
            user_dir: str =  yaml_us['user_dir']['gaeac6']
            print(f'From try, user_dir is: {user_dir}')
            vars_dict['user_dir'] = user_dir
        #if user_dir not found in yaml, use cwd
        except Exception as e:
            print(e)
            cwd = os.getcwd()
            user_dir: str = cwd
            print(f'From except, user_dir is: {user_dir}')
            vars_dict['user_dir'] = user_dir

    #Try and use machine_id to generate ecflow dir and add to dictionary
    if machine_id == 'wcoss2':
        try:
            ecf_dir: str = f'/lfs/h2/{org}/{user_group}/noscrub/{user}/ecflow'
            print(f'ecflow directory is: {ecf_dir}')
            vars_dict['ecf_dir'] = ecf_dir
        #if ecf directory is not generated, raise KeyError
        except Exception as e:
            print(e)
            raise KeyError("ERROR: ecflow directory not genereated!")
        #Try and use machine_id to generate package home and ecf_files and add to dictionary
        try:
            pack_home: str = yaml_us['pack_home']['wcoss2']
            print(f'Package home from yaml is: {pack_home}')
            vars_dict['PACKAGEHOME'] = pack_home
            pack_home: str = f'/lfs/h2/{org}/{user_group}/noscrub/{user}/nwdev/packages/aqm.{AQM_version}'
            ecf_files: str = f'{pack_home}/ecf'
            print(f'ecf_files is: {ecf_files}')
            vars_dict['ECF_FILES'] = ecf_files  
        #if package home and ecf_files are not generated, raise KeyError
        except Exception as e:
            print(e)
            pack_home: str = f'/lfs/h2/{org}/{user_group}/noscrub/{user}/nwdev/packages/aqm.{AQM_version}'
            vars_dict['PACKAGEHOME'] = pack_home
            print(f'From exception, packagehom is: {pack_home}. This is based on NCO standards. To move past error, copy paste this path into your yaml for the variable pack_home.')
            raise KeyError("ERROR: packagehome not genereated!")
        #Try and use machine_id to generate output directory and add to dictionary
        try:
            out_dir: str = f'/lfs/h2/{org}/ptmp/{user}/ecflow_aqm/para/output/prod/today'
            print(f'output directory is: {out_dir}')
            vars_dict['OUTPUTDIR'] = out_dir
        #if output directory is not generated, raise KeyError
        except Exception as e:
            print(e)
            raise KeyError("ERROR: output directory not genereated!")
    #Try and use machine_id to generate ecflow dir and add to dictionary
    elif machine_id == 'hera':
        try:
            ecf_dir: str = f'/scratch2/{org}/{user_group}/{user}'
            print(f'ecflow directory is: {ecf_dir}')
            vars_dict['ecf_dir'] = ecf_dir
        #if ecf directory is not generated, raise KeyError
        except Exception as e:
            print(e)
            raise KeyError("ERROR: ecflow directory not genereated!")
        #Try and use machine_id to generate package home and ecf_files
        #and add to dictionary
        try:
            pack_home: str = yaml_us['pack_home']['hera']
            print(f'packagehome is: {pack_home}')
            vars_dict['PACKAGEHOME'] = pack_home
            ecf_files: str = f'{pack_home}/ecf'
            print(f'ecf_files is: {ecf_files}')
            vars_dict['ECF_FILES'] = ecf_files
        #if package home and ecf_files are not generated, raise KeyError
        except Exception as e:
            print(e)
            pack_home: str = f'/scratch2/NCEPDEV/{org}/{user_group}/{user}/nwdev/packages/aqm.{AQM_version}'
            vars_dict['PACKAGEHOME'] = pack_home
            print(f'From exception, packagehom is: {pack_home}. This is based on NCO standards. To move past error, copy paste this path into your yaml for the variable pack_home.')
            raise KeyError("ERROR: packagehome not genereated!")
        #Try and use machine_id to generate output directory
        #and add to dictionary
        try:
            out_dir: str = f'/scratch2/{org}/{user}/ecflow_aqm/para/output/prod/today'
            print(f'output directory is: {out_dir}')
            vars_dict['OUTPUTDIR'] = out_dir
        #if output directory is not generated, raise KeyError
        except Exception as e:
            print(e)
            raise KeyError("ERROR: output directory not genereated!")
    #Try and use machine_id to generate ecflow dir and add to dictionary
    elif machine_id == 'gaeac6':
        try:
            ecf_dir: str = f'/gpfs/f6/{project}/scratch/{user}/noscrub/{user}/ecflow'
            print(f'ecflow directory is: {ecf_dir}')
            vars_dict['ecf_dir'] = ecf_dir
        #if ecf directory is not generated, raise KeyError
        except Exception as e:
            print(e)
            raise KeyError("ERROR: ecflow directory not genereated!")
        #Try and use machine_id to generate package home and ecf_files
        #and add to dictionary
        
        try:
            pack_home: str = yaml_us['pack_home']['gaeac6']
            print(f'packagehome is: {pack_home}')
            vars_dict['PACKAGEHOME'] = pack_home
            ecf_files: str = f'{pack_home}/ecf'
            print(f'ecf_files is: {ecf_files}')
            vars_dict['ECF_FILES'] = ecf_files
        #if package home and ecf_files are not generated, raise KeyError
        except Exception as e:
            print(e)
            pack_home: str = f'/gpfs/f6/{project}/world-shared/{user}/nwdev/packages/aqm.{AQM_version}'
            vars_dict['PACKAGEHOME'] = pack_home
            print(f'From exception, packagehom is: {pack_home}. This is based on NCO standards. To move past error, copy paste this path into your yaml for the variable pack_home.')
            raise KeyError("ERROR: packagehome not genereated!")
        #Try and use machine_id to generate output directory and add to dictionary
        try:
            out_dir: str = f'/gpfs/f6/{project}/scratch/{user}/ecflow_aqm/para/output/prod/today'
            print(f'output directory is: {out_dir}')
            vars_dict['OUTPUTDIR'] = out_dir
        #if output directory is not generated, raise KeyError
        except Exception as e:
            print(e)
            raise KeyError("ERROR: output directory not genereated!")
  
    #The path to user_settings.sh should be in /ush, the same directoary as this script
    set_ecflow_path = './setup_ecflow.sh'
    #Source setup_ecflow.sh to get the ECF_INCLUDE path
    set_ecflow_process = subprocess.Popen(f'source {set_ecflow_path} && printenv | grep -E "ECF_INCLUDE"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    set_ecflow_stdout, set_ecflow_stderr = set_ecflow_process.communicate()
    #Check for error in retrieving the ECF_INCLUDE path 
    if set_ecflow_process.returncode != 0:
        raise KeyError(f"Error: {set_ecflow_stderr.decode()}")
        print(f"output: {set_ecflow_stdout.decode()}")
    #Add ECF_INCLUDE to the dictionary
    for line in set_ecflow_stdout.decode().splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            vars_dict['ECF_INCLUDE'] = value

    return vars_dict

#generate customized ecflow def file
def def_file_generate(defs, vars_dict):
    """
    def_file_generate() creates ecflow suites, families, tasks, etc. 
    based on the the run type and variable options in the dictionary
    (vars_dict['RUN_TYPE']) from user_set_check(). 
    """
    #Create ecflow Defs class
    defs = ecf.Defs()
    #Generate ecflow suite definitions for nco 
    if vars_dict['RUN_TYPE'] == 'nco':
        #add nco_aqm suite
        suite = defs.add_suite('nco_aqm')
        #add primary family and packagehome to suite
        defs.nco_aqm += ecf.Edit(PACKAGEHOME = vars_dict['PACKAGEHOME'])
        f_primary = suite.add_family('primary')
        defs.nco_aqm.primary += [ecf.Edit(NET = vars_dict['NET']),
            ecf.Edit(RUN = vars_dict['RUN']),
            ecf.Edit(PROJ = vars_dict['PROJ']),
            ecf.Edit(PROJENVIR = vars_dict['PROJENVIR']),
            ecf.Edit(MACHINE_SITE = vars_dict['MACHINE_SITE']),
            ecf.Edit(ENVIR = vars_dict['ENVIR']),
            ecf.Edit(QUEUE = vars_dict['QUEUE']),
            ecf.Edit(QUEUE_ARCH = vars_dict['QUEUE_ARCH']),
            ecf.Edit(OUTPUTDIR = vars_dict['OUTPUTDIR']),
            ecf.Edit(ECF_INCLUDE = vars_dict['ECF_INCLUDE'])]
        cyc_list = vars_dict['CYC']
        f_hr_list = vars_dict['HOURS']
        #Create a list of restart frequencies
        restart_hr = int(vars_dict['RESTART_FREQ'])
        restart_list = []
        for j in range(len(f_hr_list)):
            print(f_hr_list[j])
            if f_hr_list[j]==restart_hr:
                restart_freq = 1
                restart_list.append(restart_freq)
            else:
                restart_freq = (int(f_hr_list[j]/restart_hr) -1)
                restart_list.append(restart_freq)
        #initialize event list
        event_num_list = []
        #Loop through cycles and generate tasks for nco_aqm
        for i in range(len(cyc_list)):
             #Calculate event generation based on forecast hours and restart frequencies
            event_num = int(f_hr_list[i] + 1 + restart_list[i])
            event_num_list.append(event_num)
            #Create cycle family
            f_cyc = defs.nco_aqm.primary.add_family(str(cyc_list[i]).zfill(2))
            f_cyc += [ecf.Edit(CYC=str(cyc_list[i]).zfill(2))]
            tsk_cyc_end = f_cyc.add_task('cycle_end')
            tsk_cyc_end += [ecf.Edit(ECF_FILES='%PACKAGEHOME%/ecf')]
            if cyc_list[i] == 0:
                tsk_cyc_end += [ecf.Cron('23:00')]
                #create aqm family
                f_aqm = f_cyc.add_family('aqm')
                #create version family & edit ECF_FILES
                f_v1 = f_aqm.add_family('v1.0')
                f_v1 += [ecf.Edit(ECF_FILES='%PACKAGEHOME%/ecf')]
                #create nexus family
                f_nexus = f_v1.add_family('nexus')
                #create 0-5 nexus emission tasks, the nexus post split, and complete triggers
                for k in range(6):
                    tsk_jaqm_nex_emis = f_nexus.add_task('jaqm_nexus_emission_0'+str(k))
                    tsk_jaqm_nex_emis += [ecf.Edit(NSPT = '0'+str(k)), ecf.Trigger('TIME >= 0142 and TIME < 0742')]
                    f_nexus += [ecf.Task('jaqm_nexus_post_split',
                        ecf.Trigger("""./jaqm_nexus_emission_00==complete and ./jaqm_nexus_emission_01==complete and ./jaqm_nexus_emission_02==complete and 
                        ./jaqm_nexus_emission_03==complete and./jaqm_nexus_emission_04==complete and ./jaqm_nexus_emission_05==complete"""))]
                #create prep family
                f_prep = f_v1.add_family('prep') 
                f_prep += [ecf.Task('jaqm_make_ics',
                    ecf.Trigger('TIME >= 0142 and TIME < 0742'))]
                f_prep += [ecf.Task('jaqm_make_lbcs',
                    ecf.Trigger('TIME >= 0142 and TIME < 0742'))]
                f_prep += [ecf.Task('jaqm_ics',
                    ecf.Trigger('./jaqm_make_ics==complete'))]
                f_prep += [ecf.Task('jaqm_lbcs',
                    ecf.Trigger('./jaqm_make_lbcs==complete and ./jaqm_make_ics==complete'))]
                #create point source fire emission family
                f_pts_fire_emis = f_v1.add_family('pts_fire_emis')
                f_pts_fire_emis += [ecf.Task('jaqm_point_source',
                        ecf.Trigger('TIME >= 0142 and TIME < 0742'))]
                f_pts_fire_emis += [ecf.Task('jaqm_fire_emission',
                        ecf.Trigger('TIME >= 0142 and TIME < 0742'))]
                #create forecast family
                f_forecast = f_v1.add_family('forecast')
                f_forecast += [ecf.Task('jaqm_forecast',
                    ecf.Trigger('../nexus==complete and ../prep==complete and ../pts_fire_emis==complete'),
                    ecf.Event(1, 'release_manager'))]
                f_forecast += [ecf.Task('jaqm_forecast_manager',
                    ecf.Trigger('./jaqm_forecast:release_manager'))]
                #create forecast manager events 
                for j in range(event_num_list[i]):
                    if j==0:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(j+1, 'restart_gp1_rdy')]
                    else:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(j+1, '00'+ str(j-1)+'_rdy')]
                #create post family
                f_post = f_v1.add_family('post')
                for j in range(event_num_list[i]-1):
                    f_post += [ecf.Task('jaqm_post_f'+str(j).zfill(3),
                        ecf.Edit(FHR = str(j).zfill(3)),
                        ecf.Trigger('../forecast==complete'))]
                #create product family
                f_product = f_v1.add_family('product')
                f_product += [ecf.Task('jaqm_pre_post_stat',
                    ecf.Trigger('../forecast==complete'))]
                f_product += [ecf.Task('jaqm_post_stat_o3',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_post_stat_pm25',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_bias_correction_o3',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_bias_correction_pm25',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
            elif cyc_list[i] ==6:
                tsk_cyc_end += [ecf.Cron('05:00')]
                #create aqm family
                f_aqm = f_cyc.add_family('aqm')
                #create version family & edit ECF_FILES
                f_v1 = f_aqm.add_family('v1.0')
                f_v1 += [ecf.Edit(ECF_FILES='%PACKAGEHOME%/ecf')]
                #create nexus family
                f_nexus = f_v1.add_family('nexus')
                #create 0-5 nexus emission tasks, the nexus post split, and complete triggers
                for j in range(6):
                    tsk_jaqm_nex_emis = f_nexus.add_task('jaqm_nexus_emission_0'+str(j))
                    tsk_jaqm_nex_emis += [ecf.Edit(NSPT = '0'+str(j))]
                    tsk_jaqm_nex_emis += [ecf.Trigger('TIME >= 0742 and TIME < 1342')]
                    f_nexus += [ecf.Task('jaqm_nexus_post_split',
                        ecf.Trigger("""./jaqm_nexus_emission_00==complete and ./jaqm_nexus_emission_01==complete and ./jaqm_nexus_emission_02==complete and 
                        ./jaqm_nexus_emission_03==complete and./jaqm_nexus_emission_04==complete and ./jaqm_nexus_emission_05==complete"""))]
                #create prep family
                f_prep = f_v1.add_family('prep') 
                f_prep += [ecf.Task('jaqm_make_ics',
                    ecf.Trigger('TIME >= 0742 and TIME < 1342'))]
                f_prep += [ecf.Task('jaqm_make_lbcs',
                    ecf.Trigger('TIME >= 0742 and TIME < 1342'))]
                f_prep += [ecf.Task('jaqm_ics',
                    ecf.Trigger('./jaqm_make_ics==complete'))]
                f_prep += [ecf.Task('jaqm_lbcs',
                    ecf.Trigger('./jaqm_make_lbcs==complete and ./jaqm_make_ics==complete'))]
                #create point source fire emission family
                f_pts_fire_emis = f_v1.add_family('pts_fire_emis')
                f_pts_fire_emis += [ecf.Task('jaqm_point_source',
                        ecf.Trigger('TIME >= 0742 and TIME < 1342'))]
                f_pts_fire_emis += [ecf.Task('jaqm_fire_emission',
                        ecf.Trigger('TIME >= 0742 and TIME < 1342'))]
                #create forecast family
                f_forecast = f_v1.add_family('forecast')
                f_forecast += [ecf.Task('jaqm_forecast',
                    ecf.Trigger('../nexus==complete and ../prep==complete and ../pts_fire_emis==complete'),
                    ecf.Event(1, 'release_manager'))]
                f_forecast += [ecf.Task('jaqm_forecast_manager',
                    ecf.Trigger('./jaqm_forecast:release_manager'))]
                for j in range(event_num_list[i]):
                    if j<restart_list[i]: 
                        f_forecast.jaqm_forecast_manager += [ecf.Event(j+1, 'restart_gp'+str(j+1)+'_rdy')]
                    else:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(j+1, str(j-restart_list[i]).zfill(3)+'_rdy')]
                #create post family
                f_post = f_v1.add_family('post')
                for i in range(f_hr_list[i]+1):
                    f_post += [ecf.Task('jaqm_post_f'+str(i).zfill(3),
                        ecf.Edit(FHR = str(i).zfill(3)),
                        ecf.Trigger('../forecast==complete'))]
                #create product family
                f_product = f_v1.add_family('product')
                f_product += [ecf.Task('jaqm_pre_post_stat',
                    ecf.Trigger('../forecast==complete'))]
                f_product += [ecf.Task('jaqm_post_stat_o3',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_post_stat_pm25',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_bias_correction_o3',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_bias_correction_pm25',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
            elif cyc_list[i] ==12:
                tsk_cyc_end += [ecf.Cron('11:00')]
                #create aqm family
                f_aqm = f_cyc.add_family('aqm')
                #create version family & edit ECF_FILES
                f_v1 = f_aqm.add_family('v1.0')
                f_v1 += [ecf.Edit(ECF_FILES='%PACKAGEHOME%/ecf')]
                #create nexus family
                f_nexus = f_v1.add_family('nexus')
                #create 0-5 nexus emission tasks, the nexus post split, and complete triggers
                for j in range(6):
                    tsk_jaqm_nex_emis = f_nexus.add_task('jaqm_nexus_emission_0'+str(j))
                    tsk_jaqm_nex_emis += [ecf.Edit(NSPT = '0'+str(j))]
                    tsk_jaqm_nex_emis += [ecf.Trigger('TIME >= 1342 and TIME < 1942')]
                f_nexus += [ecf.Task('jaqm_nexus_post_split',
                    ecf.Trigger("""./jaqm_nexus_emission_00==complete and ./jaqm_nexus_emission_01==complete and ./jaqm_nexus_emission_02==complete and 
                    ./jaqm_nexus_emission_03==complete and./jaqm_nexus_emission_04==complete and ./jaqm_nexus_emission_05==complete"""))]
                #create prep family
                f_prep = f_v1.add_family('prep') 
                f_prep += [ecf.Task('jaqm_make_ics',
                    ecf.Trigger('TIME >= 1342 and TIME < 1942'))]
                f_prep += [ecf.Task('jaqm_make_lbcs',
                    ecf.Trigger('TIME >= 1342 and TIME < 1942'))]
                f_prep += [ecf.Task('jaqm_ics',
                    ecf.Trigger('./jaqm_make_ics==complete'))]
                f_prep += [ecf.Task('jaqm_lbcs',
                    ecf.Trigger('./jaqm_make_lbcs==complete and ./jaqm_make_ics==complete'))]
                #create point source fire emission family
                f_pts_fire_emis = f_v1.add_family('pts_fire_emis')
                f_pts_fire_emis += [ecf.Task('jaqm_point_source',
                        ecf.Trigger('TIME >= 1342 and TIME < 1942'))]
                f_pts_fire_emis += [ecf.Task('jaqm_fire_emission',
                        ecf.Trigger('TIME >= 1342 and TIME < 1942'))]
                #create forecast family
                f_forecast = f_v1.add_family('forecast')
                f_forecast += [ecf.Task('jaqm_forecast',
                    ecf.Trigger('../nexus==complete and ../prep==complete and ../pts_fire_emis==complete'),
                    ecf.Event(1, 'release_manager'))]
                f_forecast += [ecf.Task('jaqm_forecast_manager',
                    ecf.Trigger('./jaqm_forecast:release_manager'))]
                for j in range(event_num_list[i]):
                    if j<restart_list[i]: 
                        f_forecast.jaqm_forecast_manager += [ecf.Event(j+1, 'restart_gp'+str(j+1)+'_rdy')]
                    else:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(j+1, str(j-restart_list[i]).zfill(3)+'_rdy')]
                #create post family
                f_post = f_v1.add_family('post')
                for i in range(f_hr_list[i]+1):
                    f_post += [ecf.Task('jaqm_post_f'+str(i).zfill(3),
                        ecf.Edit(FHR = str(i).zfill(3)),
                        ecf.Trigger('../forecast==complete'))]
                #create product family
                f_product = f_v1.add_family('product')
                f_product += [ecf.Task('jaqm_pre_post_stat',
                    ecf.Trigger('../forecast==complete'))]
                f_product += [ecf.Task('jaqm_post_stat_o3',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_post_stat_pm25',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_bias_correction_o3',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_bias_correction_pm25',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
            elif cyc_list[i] == 18:
                tsk_cyc_end += [ecf.Cron('17:00')]
                #create aqm family
                f_aqm = f_cyc.add_family('aqm')
                #create version family & edit ECF_FILES
                f_v1 = f_aqm.add_family('v1.0')
                f_v1 += [ecf.Edit(ECF_FILES='%PACKAGEHOME%/ecf')]
                #create nexus family
                f_nexus = f_v1.add_family('nexus')
                #create 0-5 nexus emission tasks, the nexus post split, and complete triggers
                for j in range(6):
                    tsk_jaqm_nex_emis = f_nexus.add_task('jaqm_nexus_emission_0'+str(j))
                    tsk_jaqm_nex_emis += [ecf.Edit(NSPT = '0'+str(j))]
                    tsk_jaqm_nex_emis += [ecf.Trigger('TIME >= 1942 and TIME < 2342')]
                f_nexus += [ecf.Task('jaqm_nexus_post_split',
                    ecf.Trigger("""./jaqm_nexus_emission_00==complete and ./jaqm_nexus_emission_01==complete and ./jaqm_nexus_emission_02==complete and 
                    ./jaqm_nexus_emission_03==complete and./jaqm_nexus_emission_04==complete and ./jaqm_nexus_emission_05==complete"""))]
                #create prep family
                f_prep = f_v1.add_family('prep') 
                f_prep += [ecf.Task('jaqm_make_ics',
                    ecf.Trigger('TIME >= 1942 and TIME < 2342'))]
                f_prep += [ecf.Task('jaqm_make_lbcs',
                    ecf.Trigger('TIME >= 1942 and TIME < 2342'))]
                f_prep += [ecf.Task('jaqm_ics',
                    ecf.Trigger('./jaqm_make_ics==complete'))]
                f_prep += [ecf.Task('jaqm_lbcs',
                    ecf.Trigger('./jaqm_make_lbcs==complete and ./jaqm_make_ics==complete'))]
                #create point source fire emission family
                f_pts_fire_emis = f_v1.add_family('pts_fire_emis')
                f_pts_fire_emis += [ecf.Task('jaqm_point_source',
                        ecf.Trigger('TIME >= 1942 and TIME < 2342'))]
                f_pts_fire_emis += [ecf.Task('jaqm_fire_emission',
                        ecf.Trigger('TIME >= 1942 and TIME < 2342'))]
                #create forecast family
                f_forecast = f_v1.add_family('forecast')
                f_forecast += [ecf.Task('jaqm_forecast',
                    ecf.Trigger('../nexus==complete and ../prep==complete and ../pts_fire_emis==complete'),
                    ecf.Event(1, 'release_manager'))]
                f_forecast += [ecf.Task('jaqm_forecast_manager',
                    ecf.Trigger('./jaqm_forecast:release_manager'))]
                #create forecast manager events 
                for j in range(event_num_list[i]):
                    if j==0:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(j+1, 'restart_gp1_rdy')]
                    else:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(j+1, '00'+ str(j-1)+'_rdy')]
                #create post family
                f_post = f_v1.add_family('post')
                for j in range(event_num_list[i]-1):
                    f_post += [ecf.Task('jaqm_post_f'+str(j).zfill(3),
                        ecf.Edit(FHR = str(j).zfill(3)),
                        ecf.Trigger('../forecast==complete'))]
                #create product family
                f_product = f_v1.add_family('product')
                f_product += [ecf.Task('jaqm_pre_post_stat',
                    ecf.Trigger('../forecast==complete'))]
                f_product += [ecf.Task('jaqm_post_stat_o3',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_post_stat_pm25',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_bias_correction_o3',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_bias_correction_pm25',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
            else:
                raise ValueError("ERROR: Cycle value is incorrect.")

    #Generate ecflow suite definitions for test 
    elif vars_dict['RUN_TYPE'] == 'test':
        #create test_aqm suite based on run_type
        suite = defs.add_suite('test_aqm') 
        #add packagehome & primary family
        defs.test_aqm += ecf.Edit(PACKAGEHOME = vars_dict['PACKAGEHOME'])
        f_primary = suite.add_family('primary')
        #add edits to primary family
        defs.test_aqm.primary += [ecf.Edit(NET = vars_dict['NET']),
            ecf.Edit(RUN = vars_dict['RUN']),
            ecf.Edit(PROJ = vars_dict['PROJ']),
            ecf.Edit(PROJENVIR = vars_dict['PROJENVIR']),
            ecf.Edit(MACHINE_SITE = vars_dict['MACHINE_SITE']),
            ecf.Edit(ENVIR = vars_dict['ENVIR']),
            ecf.Edit(QUEUE = vars_dict['QUEUE']),
            ecf.Edit(QUEUE_ARCH = vars_dict['QUEUE_ARCH']),
            ecf.Edit(OUTPUTDIR = vars_dict['OUTPUTDIR']),
            ecf.Edit(ECF_INCLUDE = vars_dict['ECF_INCLUDE'])]
        cyc_list = vars_dict['CYC']
        f_hr_list = vars_dict['HOURS']
        #Create a list of restart frequencies
        restart_hr = int(vars_dict['RESTART_FREQ'])
        restart_list = []
        for j in range(len(f_hr_list)):
            if f_hr_list[j]==restart_hr:
                restart_freq = 1
                restart_list.append(restart_freq)
            else:
                restart_freq = (int(f_hr_list[j]/restart_hr) -1)
                restart_list.append(restart_freq)
        #initialize event list
        event_num_list = []
        #Create cycle task
        for i in range(len(cyc_list)):
            #calculate event numbers within cycle loop
            event_num = int(f_hr_list[i] + 1 + restart_list[i])
            event_num_list.append(event_num)
            f_cyc = defs.test_aqm.primary.add_family(str(cyc_list[i]).zfill(2))
            f_cyc += [ecf.Edit(CYC=str(cyc_list[i]).zfill(2))]
            tsk_cyc_end = f_cyc.add_task('cycle_end')
            tsk_cyc_end += [ecf.Edit(ECF_FILES='%PACKAGEHOME%/ecf')]
            if cyc_list[i] == 0:
                tsk_cyc_end += [ecf.Cron('23:00')]
                #create aqm family
                f_aqm = f_cyc.add_family('aqm')
                #create version family & edit ECF_FILES
                f_v1 = f_aqm.add_family('v1.0')
                f_v1 += [ecf.Edit(ECF_FILES='%PACKAGEHOME%/ecf')]
                #create nexus family
                f_nexus = f_v1.add_family('nexus')
                #create 0-5 nexus emission tasks, the nexus post split, and complete triggers
                for j in range(6):
                    tsk_jaqm_nex_emis = f_nexus.add_task('jaqm_nexus_emission_0'+str(j))
                    tsk_jaqm_nex_emis += [ecf.Edit(NSPT = '0'+str(j))]
                    #tsk_jaqm_nex_emis += [ecf.Trigger('TIME >= 0142 and TIME < 0742')]
                f_nexus += [ecf.Task('jaqm_nexus_post_split',
                    ecf.Trigger("""./jaqm_nexus_emission_00==complete and ./jaqm_nexus_emission_01==complete and ./jaqm_nexus_emission_02==complete and  ./jaqm_nexus_emission_03==complete and./jaqm_nexus_emission_04==complete and ./jaqm_nexus_emission_05==complete"""))]
                #create prep family
                f_prep = f_v1.add_family('prep') 
                f_prep += [ecf.Task('jaqm_make_ics')]
                f_prep += [ecf.Task('jaqm_make_lbcs')]
                f_prep += [ecf.Task('jaqm_ics',
                    ecf.Trigger('./jaqm_make_ics==complete'))]
                f_prep += [ecf.Task('jaqm_lbcs',
                    ecf.Trigger('./jaqm_make_lbcs==complete and ./jaqm_make_ics==complete'))]
                #create point source fire emission family
                f_pts_fire_emis = f_v1.add_family('pts_fire_emis')
                f_pts_fire_emis += [ecf.Task('jaqm_point_source')]
                f_pts_fire_emis += [ecf.Task('jaqm_fire_emission')]
                #create forecast family
                f_forecast = f_v1.add_family('forecast')
                f_forecast += [ecf.Task('jaqm_forecast',
                    ecf.Trigger('../nexus==complete and ../prep==complete and ../pts_fire_emis==complete'),
                    ecf.Event(1, 'release_manager'))]
                f_forecast += [ecf.Task('jaqm_forecast_manager',
                    ecf.Trigger('./jaqm_forecast:release_manager'))]
                #create forecast manager events 
                for j in range(event_num_list[i]):
                    if j==0:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(j+1, 'restart_gp1_rdy')]
                    else:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(j+1, '00'+ str(j-1)+'_rdy')]
                #create post family
                f_post = f_v1.add_family('post')
                for j in range(event_num_list[i]-1):
                    f_post += [ecf.Task('jaqm_post_f'+str(j).zfill(3),
                        ecf.Edit(FHR = str(j).zfill(3)),
                        ecf.Trigger('../forecast==complete'))]
                #create product family
                f_product = f_v1.add_family('product')
                f_product += [ecf.Task('jaqm_pre_post_stat',
                    ecf.Trigger('../forecast==complete'))]
                f_product += [ecf.Task('jaqm_post_stat_o3',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_post_stat_pm25',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_bias_correction_o3',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_bias_correction_pm25',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
            else:
                raise ValueError("ERROR: Cycle value is incorrect.")                            

    #Generate ecflow suite definitions for user 
    elif vars_dict['RUN_TYPE'] == 'user':
        #create user_aqm suite
        suite = defs.add_suite('user_aqm')
        #Add primary family and packagehome
        defs.user_aqm += ecf.Edit(PACKAGEHOME = vars_dict['PACKAGEHOME'])
        f_primary = suite.add_family('primary')
        #Add edits to primary family
        defs.user_aqm.primary += [ecf.Edit(NET = vars_dict['NET']),
            ecf.Edit(RUN = vars_dict['RUN']),
            ecf.Edit(PROJ = vars_dict['PROJ']),
            ecf.Edit(PROJENVIR = vars_dict['PROJENVIR']),
            ecf.Edit(MACHINE_SITE = vars_dict['MACHINE_SITE']),
            ecf.Edit(ENVIR = vars_dict['ENVIR']),
            ecf.Edit(QUEUE = vars_dict['QUEUE']),
            ecf.Edit(QUEUE_ARCH = vars_dict['QUEUE_ARCH']),
            ecf.Edit(OUTPUTDIR = vars_dict['OUTPUTDIR']),
            ecf.Edit(ECF_INCLUDE = vars_dict['ECF_INCLUDE'])]
        cyc_list = vars_dict['CYC']
        f_hr_list = vars_dict['HOURS']
        #Create a list of restart frequencies
        restart_hr = int(vars_dict['RESTART_FREQ'])
        restart_list = []
        for j in range(len(f_hr_list)):
            if f_hr_list[j]==restart_hr:
                restart_freq = 1
                restart_list.append(restart_freq)
            else:
                restart_freq = (int(f_hr_list[j]/restart_hr) -1)
                restart_list.append(restart_freq)
        #initialize event list
        event_num_list = []
        #Loop through cycles and generate tasks for nco_aqm
        for i in range(len(cyc_list)):
            #Calculate event generation based on forecast hours and restart frequencies
            event_num = int(f_hr_list[i] + 1 + restart_list[i])
            event_num_list.append(event_num)
            #create cycle family
            f_cyc = defs.user_aqm.primary.add_family(str(cyc_list[i]).zfill(2))
            f_cyc += [ecf.Edit(CYC=str(cyc_list[i]).zfill(2))]
            tsk_cyc_end = f_cyc.add_task('cycle_end')
            tsk_cyc_end += [ecf.Edit(ECF_FILES='%PACKAGEHOME%/ecf')]
            if cyc_list[i] == 0:
                tsk_cyc_end += [ecf.Cron('23:00')]
                #create aqm family
                f_aqm = f_cyc.add_family('aqm')
                #create version family & edit ECF_FILES
                f_v1 = f_aqm.add_family('v1.0')
                f_v1 += [ecf.Edit(ECF_FILES='%PACKAGEHOME%/ecf')]
                #create nexus family
                f_nexus = f_v1.add_family('nexus')
                #create 0-5 nexus emission tasks, the nexus post split, and complete triggers
                for j in range(6):
                    tsk_jaqm_nex_emis = f_nexus.add_task('jaqm_nexus_emission_0'+str(j))
                    tsk_jaqm_nex_emis += [ecf.Edit(NSPT = '0'+str(j)), ecf.Trigger('TIME >= 0142 and TIME < 0742')]
                    f_nexus += [ecf.Task('jaqm_nexus_post_split',
                        ecf.Trigger("""./jaqm_nexus_emission_00==complete and ./jaqm_nexus_emission_01==complete and ./jaqm_nexus_emission_02==complete and 
                        ./jaqm_nexus_emission_03==complete and./jaqm_nexus_emission_04==complete and ./jaqm_nexus_emission_05==complete"""))]
                #create prep family
                f_prep = f_v1.add_family('prep') 
                f_prep += [ecf.Task('jaqm_make_ics',
                    ecf.Trigger('TIME >= 0142 and TIME < 0742'))]
                f_prep += [ecf.Task('jaqm_make_lbcs',
                    ecf.Trigger('TIME >= 0142 and TIME < 0742'))]
                f_prep += [ecf.Task('jaqm_ics',
                    ecf.Trigger('./jaqm_make_ics==complete'))]
                f_prep += [ecf.Task('jaqm_lbcs',
                    ecf.Trigger('./jaqm_make_lbcs==complete and ./jaqm_make_ics==complete'))]
                #create point source fire emission family
                f_pts_fire_emis = f_v1.add_family('pts_fire_emis')
                f_pts_fire_emis += [ecf.Task('jaqm_point_source',
                        ecf.Trigger('TIME >= 0142 and TIME < 0742'))]
                f_pts_fire_emis += [ecf.Task('jaqm_fire_emission',
                        ecf.Trigger('TIME >= 0142 and TIME < 0742'))]
                #create forecast family
                f_forecast = f_v1.add_family('forecast')
                f_forecast += [ecf.Task('jaqm_forecast',
                    ecf.Trigger('../nexus==complete and ../prep==complete and ../pts_fire_emis==complete'),
                    ecf.Event(1, 'release_manager'))]
                f_forecast += [ecf.Task('jaqm_forecast_manager',
                    ecf.Trigger('./jaqm_forecast:release_manager'))]
                #create forecast manager events 
                for j in range(event_num_list[i]):
                    if j==0:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(j+1, 'restart_gp1_rdy')]
                    else:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(j+1, '00'+ str(j-1)+'_rdy')]
                #create post family
                f_post = f_v1.add_family('post')
                for j in range(event_num_list[i]-1):
                    f_post += [ecf.Task('jaqm_post_f'+str(j).zfill(3),
                        ecf.Edit(FHR = str(j).zfill(3)),
                        ecf.Trigger('../forecast==complete'))]
                #create product family
                f_product = f_v1.add_family('product')
                f_product += [ecf.Task('jaqm_pre_post_stat',
                    ecf.Trigger('../forecast==complete'))]
                f_product += [ecf.Task('jaqm_post_stat_o3',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_post_stat_pm25',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_bias_correction_o3',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_bias_correction_pm25',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
            elif cyc_list[i] ==6:
                tsk_cyc_end += [ecf.Cron('05:00')]
                #create aqm family
                f_aqm = f_cyc.add_family('aqm')
                #create version family & edit ECF_FILES
                f_v1 = f_aqm.add_family('v1.0')
                f_v1 += [ecf.Edit(ECF_FILES='%PACKAGEHOME%/ecf')]
                #create nexus family
                f_nexus = f_v1.add_family('nexus')
                #create 0-5 nexus emission tasks, the nexus post split, and complete triggers
                for j in range(6):
                    tsk_jaqm_nex_emis = f_nexus.add_task('jaqm_nexus_emission_0'+str(j))
                    tsk_jaqm_nex_emis += [ecf.Edit(NSPT = '0'+str(j))]
                    tsk_jaqm_nex_emis += [ecf.Trigger('TIME >= 0742 and TIME < 1342')]
                    f_nexus += [ecf.Task('jaqm_nexus_post_split',
                        ecf.Trigger("""./jaqm_nexus_emission_00==complete and ./jaqm_nexus_emission_01==complete and ./jaqm_nexus_emission_02==complete and 
                        ./jaqm_nexus_emission_03==complete and./jaqm_nexus_emission_04==complete and ./jaqm_nexus_emission_05==complete"""))]
                #create prep family
                f_prep = f_v1.add_family('prep') 
                f_prep += [ecf.Task('jaqm_make_ics',
                    ecf.Trigger('TIME >= 0742 and TIME < 1342'))]
                f_prep += [ecf.Task('jaqm_make_lbcs',
                    ecf.Trigger('TIME >= 0742 and TIME < 1342'))]
                f_prep += [ecf.Task('jaqm_ics',
                    ecf.Trigger('./jaqm_make_ics==complete'))]
                f_prep += [ecf.Task('jaqm_lbcs',
                    ecf.Trigger('./jaqm_make_lbcs==complete and ./jaqm_make_ics==complete'))]
                #create point source fire emission family
                f_pts_fire_emis = f_v1.add_family('pts_fire_emis')
                f_pts_fire_emis += [ecf.Task('jaqm_point_source',
                        ecf.Trigger('TIME >= 0742 and TIME < 1342'))]
                f_pts_fire_emis += [ecf.Task('jaqm_fire_emission',
                        ecf.Trigger('TIME >= 0742 and TIME < 1342'))]
                #create forecast family
                f_forecast = f_v1.add_family('forecast')
                f_forecast += [ecf.Task('jaqm_forecast',
                    ecf.Trigger('../nexus==complete and ../prep==complete and ../pts_fire_emis==complete'),
                    ecf.Event(1, 'release_manager'))]
                f_forecast += [ecf.Task('jaqm_forecast_manager',
                    ecf.Trigger('./jaqm_forecast:release_manager'))]
                #create forecast manager family
                for j in range(event_num_list[i]):
                    if j<restart_list[i]: 
                        f_forecast.jaqm_forecast_manager += [ecf.Event(j+1, 'restart_gp'+str(j+1)+'_rdy')]
                    else:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(j+1, str(j-restart_list[i]).zfill(3)+'_rdy')]
                #create post family
                f_post = f_v1.add_family('post')
                for i in range(f_hr_list[i]+1):
                    f_post += [ecf.Task('jaqm_post_f'+str(i).zfill(3),
                        ecf.Edit(FHR = str(i).zfill(3)),
                        ecf.Trigger('../forecast==complete'))]
                #create product family
                f_product = f_v1.add_family('product')
                f_product += [ecf.Task('jaqm_pre_post_stat',
                    ecf.Trigger('../forecast==complete'))]
                f_product += [ecf.Task('jaqm_post_stat_o3',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_post_stat_pm25',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_bias_correction_o3',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_bias_correction_pm25',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
            elif cyc_list[i] ==12:
                tsk_cyc_end += [ecf.Cron('11:00')]
                #create aqm family
                f_aqm = f_cyc.add_family('aqm')
                #create version family & edit ECF_FILES
                f_v1 = f_aqm.add_family('v1.0')
                f_v1 += [ecf.Edit(ECF_FILES='%PACKAGEHOME%/ecf')]
                #create nexus family
                f_nexus = f_v1.add_family('nexus')
                #create 0-5 nexus emission tasks, the nexus post split, and complete triggers
                for j in range(6):
                    tsk_jaqm_nex_emis = f_nexus.add_task('jaqm_nexus_emission_0'+str(j))
                    tsk_jaqm_nex_emis += [ecf.Edit(NSPT = '0'+str(j))]
                    tsk_jaqm_nex_emis += [ecf.Trigger('TIME >= 1342 and TIME < 1942')]
                f_nexus += [ecf.Task('jaqm_nexus_post_split',
                    ecf.Trigger("""./jaqm_nexus_emission_00==complete and ./jaqm_nexus_emission_01==complete and ./jaqm_nexus_emission_02==complete and 
                    ./jaqm_nexus_emission_03==complete and./jaqm_nexus_emission_04==complete and ./jaqm_nexus_emission_05==complete"""))]
                #create prep family
                f_prep = f_v1.add_family('prep') 
                f_prep += [ecf.Task('jaqm_make_ics',
                    ecf.Trigger('TIME >= 1342 and TIME < 1942'))]
                f_prep += [ecf.Task('jaqm_make_lbcs',
                    ecf.Trigger('TIME >= 1342 and TIME < 1942'))]
                f_prep += [ecf.Task('jaqm_ics',
                    ecf.Trigger('./jaqm_make_ics==complete'))]
                f_prep += [ecf.Task('jaqm_lbcs',
                    ecf.Trigger('./jaqm_make_lbcs==complete and ./jaqm_make_ics==complete'))]
                #create point source fire emission family
                f_pts_fire_emis = f_v1.add_family('pts_fire_emis')
                f_pts_fire_emis += [ecf.Task('jaqm_point_source',
                        ecf.Trigger('TIME >= 1342 and TIME < 1942'))]
                f_pts_fire_emis += [ecf.Task('jaqm_fire_emission',
                        ecf.Trigger('TIME >= 1342 and TIME < 1942'))]
               #create forecast family
                f_forecast = f_v1.add_family('forecast')
                f_forecast += [ecf.Task('jaqm_forecast',
                    ecf.Trigger('../nexus==complete and ../prep==complete and ../pts_fire_emis==complete'),
                    ecf.Event(1, 'release_manager'))]
                f_forecast += [ecf.Task('jaqm_forecast_manager',
                    ecf.Trigger('./jaqm_forecast:release_manager'))]
                #create forecast manager family
                for j in range(event_num_list[i]):
                    if j<restart_list[i]: 
                        f_forecast.jaqm_forecast_manager += [ecf.Event(j+1, 'restart_gp'+str(j+1)+'_rdy')]
                    else:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(j+1, str(j-restart_list[i]).zfill(3)+'_rdy')]
                #create post family
                f_post = f_v1.add_family('post')
                for i in range(f_hr_list[i]+1):
                    f_post += [ecf.Task('jaqm_post_f'+str(i).zfill(3),
                        ecf.Edit(FHR = str(i).zfill(3)),
                        ecf.Trigger('../forecast==complete'))]
                #create product family
                f_product = f_v1.add_family('product')
                f_product += [ecf.Task('jaqm_pre_post_stat',
                    ecf.Trigger('../forecast==complete'))]
                f_product += [ecf.Task('jaqm_post_stat_o3',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_post_stat_pm25',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_bias_correction_o3',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_bias_correction_pm25',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
            elif cyc_list[i] == 18:
                tsk_cyc_end += [ecf.Cron('17:00')]
                #create aqm family
                f_aqm = f_cyc.add_family('aqm')
                #create version family & edit ECF_FILES
                f_v1 = f_aqm.add_family('v1.0')
                f_v1 += [ecf.Edit(ECF_FILES='%PACKAGEHOME%/ecf')]
                #create nexus family
                f_nexus = f_v1.add_family('nexus')
                #create 0-5 nexus emission tasks, the nexus post split, and complete triggers
                for j in range(6):
                    tsk_jaqm_nex_emis = f_nexus.add_task('jaqm_nexus_emission_0'+str(j))
                    tsk_jaqm_nex_emis += [ecf.Edit(NSPT = '0'+str(j))]
                    tsk_jaqm_nex_emis += [ecf.Trigger('TIME >= 1942 and TIME < 2342')]
                f_nexus += [ecf.Task('jaqm_nexus_post_split',
                    ecf.Trigger("""./jaqm_nexus_emission_00==complete and ./jaqm_nexus_emission_01==complete and ./jaqm_nexus_emission_02==complete and 
                    ./jaqm_nexus_emission_03==complete and./jaqm_nexus_emission_04==complete and ./jaqm_nexus_emission_05==complete"""))]
                #create prep family
                f_prep = f_v1.add_family('prep') 
                f_prep += [ecf.Task('jaqm_make_ics',
                    ecf.Trigger('TIME >= 1942 and TIME < 2342'))]
                f_prep += [ecf.Task('jaqm_make_lbcs',
                    ecf.Trigger('TIME >= 1942 and TIME < 2342'))]
                f_prep += [ecf.Task('jaqm_ics',
                    ecf.Trigger('./jaqm_make_ics==complete'))]
                f_prep += [ecf.Task('jaqm_lbcs',
                    ecf.Trigger('./jaqm_make_lbcs==complete and ./jaqm_make_ics==complete'))]
                #create point source fire emission family
                f_pts_fire_emis = f_v1.add_family('pts_fire_emis')
                f_pts_fire_emis += [ecf.Task('jaqm_point_source',
                        ecf.Trigger('TIME >= 1942 and TIME < 2342'))]
                f_pts_fire_emis += [ecf.Task('jaqm_fire_emission',
                        ecf.Trigger('TIME >= 1942 and TIME < 2342'))]
                #create forecast family
                f_forecast = f_v1.add_family('forecast')
                f_forecast += [ecf.Task('jaqm_forecast',
                    ecf.Trigger('../nexus==complete and ../prep==complete and ../pts_fire_emis==complete'),
                    ecf.Event(1, 'release_manager'))]
                f_forecast += [ecf.Task('jaqm_forecast_manager',
                    ecf.Trigger('./jaqm_forecast:release_manager'))]
                #create forecast manager family
                for j in range(event_num_list[i]):
                    if j<restart_list[i]: 
                        f_forecast.jaqm_forecast_manager += [ecf.Event(j+1, 'restart_gp'+str(j+1)+'_rdy')]
                    else:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(j+1, str(j-restart_list[i]).zfill(3)+'_rdy')]
                #create post family
                f_post = f_v1.add_family('post')
                for i in range(f_hr_list[i]+1):
                    f_post += [ecf.Task('jaqm_post_f'+str(i).zfill(3),
                        ecf.Edit(FHR = str(i).zfill(3)),
                        ecf.Trigger('../forecast==complete'))]
                #create product family
                f_product = f_v1.add_family('product')
                f_product += [ecf.Task('jaqm_pre_post_stat',
                    ecf.Trigger('../forecast==complete'))]
                f_product += [ecf.Task('jaqm_post_stat_o3',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_post_stat_pm25',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_bias_correction_o3',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
                f_product += [ecf.Task('jaqm_bias_correction_pm25',
                    ecf.Trigger('./jaqm_pre_post_stat==complete'))]
            else:
                raise ValueError("ERROR: Cycle value is incorrect.")                        

    def_file(defs)

#save ecf/defs/output.def
def def_file(defs):
    """
    def_file() generates the ecflow definition file (output.def) 
    in /ecf/defs based on the ecflow definitions from def_file_generate()
    """
    try:
        defs.save_as_defs('../ecf/defs/output.def')
        #defs.save_as_defs('/ecf/defs/output.def')
        print('output.def written')
    except Exception:
        print('Caught Error')

main()
