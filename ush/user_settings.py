
"""
This script takes check user_settings.sh for run_type.
It then reads in and check vars from the run_type based yaml.
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
    #yaml_us = yml_read()
    vars_dict = {}
    #user_set_check(yaml_us, vars_dict)
    user_set_check(vars_dict)
    defs=ecf.Defs
    def_file_generate(defs, vars_dict)
    def_file(defs)

#reads in user_set.yml
#def yml_read():
#    """Reads in user_set.yml file"""
#    try:
#        yaml_us = yaml.safe_load(Path("user_set.yml").read_text())
#        print(f" dict is: {yaml_us}")
#        return yaml_us
#    except yaml.YAMLError as exc:
#        print(exc)

#checks user_set.yaml vars & adds others 
#def user_set_check(yaml_us, vars_dict):
def user_set_check(vars_dict):
    """
    user_set_check performers 3 tasks:
    1. Read in variables set in user_settings.sh,
    the yaml based on run_type set in user_setting.sh: 
    test_aqm.yml, nco_aqm.yml, or user_aqm.yml. 
    2. Perform sanity/error checks on varibles 
    3. Save the checked variables to dictionary: vars_dict.
    """
    #get username for directory paths from environment
    user: str = os.environ['USER']
    vars_dict['user'] = user

    #get vars exported from user_settings.sh: user_group, organization, aqm_version 
    #run_type: nco, community, or testing
    #user_set_path = '/scratch2/NCEPDEV/naqfc/Anna.Smoot/git/AnnaSmoot-NOAA/AQM-Workflow/ecf_update/ush/user_settings.sh'
    user_set_path = './user_settings.sh'
    user_set_process = subprocess.Popen(f'source {user_set_path} && printenv | grep -E "run_type"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    user_set_stdout, user_set_stderr = user_set_process.communicate()

    if user_set_process.returncode != 0:
        raise KeyError(f"Error: {user_set_stderr.decode()}")
        print(f"output: {user_set_stdout.decode()}")

    for line in user_set_stdout.decode().splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            vars_dict['RUN_TYPE'] = value
            print('RUN_TYPE from US.SH')
            print(vars_dict['RUN_TYPE'])
            print(f'first vars_dict is: {vars_dict}')
    
    #read correct yaml user settings (yaml_us) based on run_type from user_settings.sh
    if vars_dict['RUN_TYPE'] == 'nco':
        try:
            yaml_us = yaml.safe_load(Path("nco_aqm.yml").read_text())
            print(f"from nco_aqm.yml, yml is: {yaml_us}")
        except yaml.YAMLError as exc:
            print(exc)
    elif vars_dict['RUN_TYPE'] == 'test':
        try:
            yaml_us = yaml.safe_load(Path("test_aqm.yml").read_text())
            print(f"from test_aqm.yml, yaml is: {yaml_us}")
        except yaml.YAMLError as exc:
            print(exc)
    else: #assume RUN_TYPE== 'user'
        try:
            yaml_us = yaml.safe_load(Path("user_aqm.yml").read_text())
            print(f"from user_aqm.yml, yaml is: {yaml_us}")
        except yaml.YAMLError as exc:
            print(exc)

    #group from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    try:
        user_group: str = yaml_us['USER_GROUP']
        print(f"USER_GROUP is: {user_group}")
        if user_group is None:
            raise TypeError("ERROR: USER_GROUP is not set. Set USER_GROUP in yaml")
        else:
           #print(f"USER_GROUP is: {user_group}")
            vars_dict['user_group'] = user_group
    except:
        raise KeyError("ERROR:Invalid USER_GROUP. Set USER_GROUP in yaml")

    #version of AQM from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    try:
        AQM_version: str = yaml_us['aqm_ver']
        vars_dict['aqm_ver'] = AQM_version
        if AQM_version is None:
            raise TypeError("ERROR: aqm_ver is not set. Set aqm_ver in yaml")
        else:
            print(f"aqm_ver is: {AQM_version}")
            vars_dict['aqm_ver'] = AQM_version
    except:
        raise KeyError("ERROR: Invalid aqm_ver. Set aqm_ver in yaml")

    #Organization from from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    try:
        org: str = yaml_us['ORG']
        if org is None:
            raise TypeError("ERROR: ORG is not set. Set ORG in yaml")
        else:
            print(f"ORG is: {org}")
            vars_dict['org'] = org
    except:
        raise KeyError("ERROR: Invalid ORG. Set ORG in yaml")


    #queue from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    try: 
        queue: str = yaml_us['QUEUE']
        if queue is None:
            raise TypeError("ERROR: QUEUE is not set. Set QUEUE in yaml")
        else:
            print(f"QUEUE is: {queue}")
            vars_dict['QUEUE'] = queue
    except:
        raise KeyError("ERROR: Invalid QUEUE. Set QUEUE in yaml")   

    #PDY - start date from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    try:
        pdy: int = str(yaml_us['PDY']).zfill(8)
        if pdy is None:
            raise TypeError("ERROR: PDY is not set. Set PDY in yaml")
        else:
            print(f"PDY is: {pdy}")
            vars_dict['pdy'] = pdy
    except:
        raise KeyError("ERROR: Invalid PDY. Set PDY in yaml")        

    #Cycles var from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    try:
        cyc: int = yaml_us['CYC']
        print(type(cyc))
        print(f'CYC is: {cyc}')
        vars_dict['CYC'] = cyc
    except:
        raise KeyError("ERROR: Invalid CYC. Set CYC in yaml")

    #Forecast hours var from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    try:
        fcst_hr: int = yaml_us['HOURS']
        print(type(fcst_hr))
        print(f'HOURS: {fcst_hr}')
        #check that cycle & forecast hours arrays are the same length
        fcst_len = len(cyc)
        print(f'Forecast hour length: {fcst_len}')
        cyc_len = len(fcst_hr)
        print(f'cycle length: {cyc_len}')
        if len(cyc) != len(fcst_hr): 
            raise ValueError("ERROR: forecast hours & cycle array lengths must match. Check HOURS and CYC in yaml")
        else:
            vars_dict['HOURS'] = fcst_hr
    except:
        raise KeyError("ERROR: Invalid forecast hours. Set HOURS in yaml")

    #Project var from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    try:
        project: str = yaml_us['PROJ']
        print(f'PROJ is: {project}')
        vars_dict['PROJ'] = project
        if project is None:
            raise TypeError("ERROR: PROJ is not set. Set PROJ in yaml")
    except:
        raise KeyError("ERROR: Invalid PROJ. Set PROJ in yaml")

    #Project environment var from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    try:
        proj_env: str = yaml_us['PROJENV']
        print(f'PROJENV is: {proj_env}')
        vars_dict['PROJENV'] = proj_env
        if proj_env is None:
            raise TypeError("ERROR: PROJENV is not set. Set PROJENV in yaml")
    except:
        raise KeyError("ERROR: Invalid PROJENV. Set PROJENV in yaml")

    #net var from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    try:
        net: str = yaml_us['NET']
        print(f'NET is: {net}')
        vars_dict['NET'] = net
        if net is None:
            raise TypeError("ERROR: NET is not set. Set NET in yaml")
    except:
        raise KeyError("ERROR: Invalid NET. Set NET in yaml")            

    #Run var from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    try:
        run: str = yaml_us['RUN']
        print(f'RUN is: {run}')
        vars_dict['RUN'] = run
        if run is None:
            raise TypeError("ERROR: RUN is not set. Set RUN in yaml")
    except:
        raise KeyError("ERROR: Invalid RUN. Set RUN in yaml")

    #environment var from yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
    try:
        envir: str = yaml_us['ENVIR']
        print(f'ENVIR is: {envir}')
        vars_dict['ENVIR'] = envir
        if envir is None:
            raise TypeError("ERROR: ENVIR is not set. Set ENVIR in yaml")
    except:
        raise KeyError("ERROR: Invalid ENVIR. Set ENVIR in yaml")

    try:
        q_arch: str = yaml_us['QUEUE_ARCH']
        print(f'QUEUE_ARCH is: {q_arch}')
        vars_dict['QUEUE_ARCH'] = q_arch
        if q_arch is None:
            raise TypeError("ERROR: QUEUE_ARCH is not set. Set QUEUE_ARCH in yaml")
    except:
        raise KeyError("ERROR: Invalid QUEUE_ARCH. Set QUEUE_ARCH in yaml")

    try:
        mach_site: str = yaml_us['MACHINE_SITE']
        print(f'MACHINE_SITE is: {mach_site}')
        vars_dict['MACHINE_SITE'] = mach_site
        if mach_site is None:
            raise TypeError("ERROR: MACHINE_SITE is not set. Set MACHINE_SITE in yaml")
    except:
        raise KeyError("ERROR: Invalid MACHINE_SITE. Set QMACHINE_SITE in yaml")

    try: 
        wf_mode: str = yaml_us['MODE']
        if wf_mode is None:
            raise TypeError("ERROR: workflow_mode is not set. Set workflow_mode in yaml")
        else:
            print(f"workflow_mode is: {wf_mode}")
            vars_dict['workflow_mode'] = wf_mode
    except:
        raise KeyError("ERROR: Invalid workflow_mode. Set workflow_mode in yaml")

    #Check the machine_id from detect_machine.sh and 
    #use it to get user_dir yaml (test_aqm.yml, nco_aqm.yml, user_aqm.yml)
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

    #Generate ecflow dir, packagehome dir, and output dir
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
            pack_home: str = f'/scratch2/NCEPDEV/{org}/{user_group}/{user}/nwdev/packages/aqm.{AQM_version}'
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
            print(f'final vars_dict before return: {vars_dict}')

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
                print("KeyError: You are on wcoss2. Please set ECF_HOST in yaml to cdecflow01 or ddecflow01")
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
    """Generate the ecflow.def file based on yaml"""
    defs = ecf.Defs()
    print(f"From def file gen func: {vars_dict}")
    if vars_dict['RUN_TYPE'] == 'nco':
        suite = defs.add_suite('nco_aqm') #or call aqm_cycled_def.py? 
        f_primary = suite.add_family('primary')
        defs.nco_aqm.primary += [ecf.Edit(PACKAGEHOME = vars_dict['PACKAGEHOME']),
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
        cyc_list = vars_dict['CYC']
        print(f'cyc_list type is: {type(cyc_list)}')
        print(f'cyc_list is: {cyc_list}')
        f_hr_list = vars_dict['HOURS']
        print(f'forecast hours type is: {type(f_hr_list)}')
        print(f'forecast hours are: {f_hr_list}')
        print(f_hr_list[1])
        #Calculate forecast hour limit for event generation
        for i in range(len(cyc_list)):
            for j in range(len(f_hr_list)):
                if cyc_list[i] == 0:
                    limit_6hr= int(f_hr_list[0] + f_hr_list[0]/6 + 2)
                if cyc_list[i] == 6:
                    limit_72hr= int(f_hr_list[1] + f_hr_list[1]/6 + 1)
                if cyc_list[i] == 12:
                    limit_72hr= int(f_hr_list[2] + f_hr_list[2]/6 + 1)
                if cyc_list[i] == 18:
                    limit_6hr= int(f_hr_list[3] + f_hr_list[3]/6 + 2)
        print(limit_6hr)
        print(limit_72hr)
        #Loop through cycles and generate tasks for nco_aqm
        for i in range(len(cyc_list)):
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
                for i in range (6):
                    tsk_jaqm_nex_emis = f_nexus.add_task('jaqm_nexus_emission_0'+str(i))
                    tsk_jaqm_nex_emis += [ecf.Edit(NSPT = '0'+str(i)), ecf.Trigger('TIME >= 0142 and TIME < 0742')]
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
                #create forecast manager events based on limit calcualted above
                for i in range(1,limit_6hr):
                    if i ==1:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(i, 'restart_gp1_rdy')]
                    else:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(i, '00'+ str(i-2)+'_rdy')]
                #create post family
                f_post = f_v1.add_family('post')
                for i in range(7):
                    f_post += [ecf.Task('jaqm_post_f00'+str(i),
                        ecf.Edit(FHR = '00'+str(i)),
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
                for i in range (6):
                    tsk_jaqm_nex_emis = f_nexus.add_task('jaqm_nexus_emission_0'+str(i))
                    tsk_jaqm_nex_emis += [ecf.Edit(NSPT = '0'+str(i))]
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
                for i in range(1,limit_72hr):
                    if i<12: 
                        j=i
                        f_forecast.jaqm_forecast_manager += [ecf.Event(i, 'restart_gp'+str(j)+'_rdy')]
                    else:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(i, '00'+ str(i-12)+'_rdy')]
                #create post family
                f_post = f_v1.add_family('post')
                for i in range(73):
                    f_post += [ecf.Task('jaqm_post_f00'+str(i),
                        ecf.Edit(FHR = '00'+str(i)),
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
                for i in range (6):
                    tsk_jaqm_nex_emis = f_nexus.add_task('jaqm_nexus_emission_0'+str(i))
                    tsk_jaqm_nex_emis += [ecf.Edit(NSPT = '0'+str(i))]
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
                for i in range (6):
                    tsk_jaqm_nex_emis = f_nexus.add_task('jaqm_nexus_emission_0'+str(i))
                    tsk_jaqm_nex_emis += [ecf.Edit(NSPT = '0'+str(i))]
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
                #create forecast manager events based on limit calcualted above
                for i in range(1,limit_6hr):
                    if i ==1:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(i, 'restart_gp1_rdy')]
                    else:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(i, '00'+ str(i-2)+'_rdy')]
                #create post family
                f_post = f_v1.add_family('post')
                for i in range(7):
                    f_post += [ecf.Task('jaqm_post_f00'+str(i),
                        ecf.Edit(FHR = '00'+str(i)),
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
    
    #Generate test_aqm for cycle 00
    elif vars_dict['RUN_TYPE'] == 'test':
        #create test_aqm suite based on run_type
        suite = defs.add_suite('test_aqm') 
        #add primary family
        f_primary = suite.add_family('primary')
        #add edits to primary family
        defs.test_aqm.primary += [ecf.Edit(PACKAGEHOME = vars_dict['PACKAGEHOME']),
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
        cyc_list = vars_dict['CYC']
        for i in range(len(cyc_list)):
            print(cyc_list[i])
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
                for i in range (6):
                    tsk_jaqm_nex_emis = f_nexus.add_task('jaqm_nexus_emission_0'+str(i))
                    tsk_jaqm_nex_emis += [ecf.Edit(NSPT = '0'+str(i))]
                    #tsk_jaqm_nex_emis += [ecf.Trigger('TIME >= 0142 and TIME < 0742')]
                f_nexus += [ecf.Task('jaqm_nexus_post_split',
                    ecf.Trigger("""./jaqm_nexus_emission_00==complete and ./jaqm_nexus_emission_01==complete and ./jaqm_nexus_emission_02==complete and 
                    ./jaqm_nexus_emission_03==complete and./jaqm_nexus_emission_04==complete and ./jaqm_nexus_emission_05==complete"""))]
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
                for i in range(1,9):
                    if i == 1:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(i, 'restart_gp1_rdy')]
                    else:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(i, '00'+ str(i-2)+'_rdy')]
                #create post family
                f_post = f_v1.add_family('post')
                for i in range(7):
                    f_post += [ecf.Task('jaqm_post_f00'+str(i),
                        ecf.Edit(FHR = '00'+str(i)),
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

    #cycle based generation of user_aqm
    else:  #assume community (configurable) run, user
        suite = defs.add_suite('user_aqm')
        f_primary = suite.add_family('primary')
        defs.user_aqm.primary += [ecf.Edit(PACKAGEHOME = vars_dict['PACKAGEHOME']),
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
        cyc_list = vars_dict['CYC']
        print(f'cyc_list type is: {type(cyc_list)}')
        print(f'cyc_list is: {cyc_list}')
        f_hr_list = vars_dict['HOURS']
        print(f'forecast hours type is: {type(f_hr_list)}')
        print(f'forecast hours are: {f_hr_list}')
        print(f_hr_list[1])
        #Calculate forecast hour limit for event generation
        for i in range(len(cyc_list)):
            for j in range(len(f_hr_list)):
                if cyc_list[i] == 0:
                    limit_6hr= int(f_hr_list[0] + f_hr_list[0]/6 + 2)
                if cyc_list[i] == 6:
                    limit_72hr= int(f_hr_list[1] + f_hr_list[1]/6 + 1)
                if cyc_list[i] == 12:
                    limit_72hr= int(f_hr_list[2] + f_hr_list[2]/6 + 1)
                if cyc_list[i] == 18:
                    limit_6hr= int(f_hr_list[3] + f_hr_list[3]/6 + 2)
        print(limit_6hr)
        print(limit_72hr)
        #Loop through cycles and generate tasks for nco_aqm
        for i in range(len(cyc_list)):
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
                for i in range (6):
                    tsk_jaqm_nex_emis = f_nexus.add_task('jaqm_nexus_emission_0'+str(i))
                    tsk_jaqm_nex_emis += [ecf.Edit(NSPT = '0'+str(i)), ecf.Trigger('TIME >= 0142 and TIME < 0742')]
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
                #create forecast manager events based on limit calcualted above
                for i in range(1,limit_6hr):
                    if i ==1:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(i, 'restart_gp1_rdy')]
                    else:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(i, '00'+ str(i-2)+'_rdy')]
                #create post family
                f_post = f_v1.add_family('post')
                for i in range(7):
                    f_post += [ecf.Task('jaqm_post_f00'+str(i),
                        ecf.Edit(FHR = '00'+str(i)),
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
                for i in range (6):
                    tsk_jaqm_nex_emis = f_nexus.add_task('jaqm_nexus_emission_0'+str(i))
                    tsk_jaqm_nex_emis += [ecf.Edit(NSPT = '0'+str(i))]
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
                for i in range(1,limit_72hr):
                    if i<12: 
                        j=i
                        f_forecast.jaqm_forecast_manager += [ecf.Event(i, 'restart_gp'+str(j)+'_rdy')]
                    else:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(i, '00'+ str(i-12)+'_rdy')]
                #create post family
                f_post = f_v1.add_family('post')
                for i in range(73):
                    f_post += [ecf.Task('jaqm_post_f00'+str(i),
                        ecf.Edit(FHR = '00'+str(i)),
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
                for i in range (6):
                    tsk_jaqm_nex_emis = f_nexus.add_task('jaqm_nexus_emission_0'+str(i))
                    tsk_jaqm_nex_emis += [ecf.Edit(NSPT = '0'+str(i))]
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
                for i in range (6):
                    tsk_jaqm_nex_emis = f_nexus.add_task('jaqm_nexus_emission_0'+str(i))
                    tsk_jaqm_nex_emis += [ecf.Edit(NSPT = '0'+str(i))]
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
                #create forecast manager events based on limit calcualted above
                for i in range(1,limit_6hr):
                    if i ==1:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(i, 'restart_gp1_rdy')]
                    else:
                        f_forecast.jaqm_forecast_manager += [ecf.Event(i, '00'+ str(i-2)+'_rdy')]
                #create post family
                f_post = f_v1.add_family('post')
                for i in range(7):
                    f_post += [ecf.Task('jaqm_post_f00'+str(i),
                        ecf.Edit(FHR = '00'+str(i)),
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

    print('definition finished!')
    def_file(defs)

#save ecf/defs/output.def
def def_file(defs):
    try:
        defs.save_as_defs('../ecf/defs/output.def')
        print('output.def written')
    except Exception:
        print('Caught Error')

main()
