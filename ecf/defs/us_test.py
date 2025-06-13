#test python-bash communication
#set user settings in this python script using os.environ
#have a bash script try to read vars from environ

import os

os.environ['RUN'] = 'aqm'
os.environ['PDY'] = '20230701'
print(f'RUN is: {os.environ["RUN"]}')
print(f'PDY is: {os.environ["PDY"]}')