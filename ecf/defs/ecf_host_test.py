#This is the user settings script

#imports
import os
#import ecflow as ecf

def main():
    user_set()

def user_set():
    #ECFlow Host Server Location
    #Before running this script, in the command line enter "module load ecflow"
    #This can be left blank if set by module load properly
    try:
        ecf_host: str = os.environ.get('ECF_HOST')
        #os.environ['ECF_HOST'] = ecf_host
        print(f'ecf_host from ENVIRON: {os.environ["ECF_HOST"]}')
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
        print(f'ecf_host from EXCEPTION: {os.environ["ECF_HOST"]}')

main()