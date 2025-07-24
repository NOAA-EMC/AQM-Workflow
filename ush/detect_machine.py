import socket
import re
import yaml

## TO EXPORT MACHINE_ID IN BASH USE: eval export $(python detect_machine.py)

def get_machine_id() -> str:
  user_hostname: str = socket.gethostname()
  MACHINE_ID: str = ""

  with open('supported_machines.yaml', 'r') as file:
      supported_machines = yaml.safe_load(file)

  for machine, item in supported_machines['supported_machines'].items():
      for reg_hn in item['regex_hostnames']:
        if re.match(reg_hn, user_hostname):
          MACHINE_ID: str = machine
          print(f'MACHINE_ID="{MACHINE_ID}"')
          pass
      
  if MACHINE_ID == "":
    raise Exception("No Match Found. Is this machine supported?")
  
  return MACHINE_ID

if __name__ == "__main__":
  get_machine_id()