#This is a Python file to generate aqm_cycled.def
#as 6hr dev testing with machine & user configurability

#imports
import ecflow as ecf
import os

#variables


#main function
def main():
    defs = ecf.Defs()
    suite(defs)
    f_primary(defs)
    f_cycle(defs)
    out_file(defs)

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



#user settings function: 
#1. reads user_setting.sh, 2. checks vars exsist, 3. checks values are good

#machine settings function: read in and check
#1. reads ________, 2. checks vars exsist, 3. checks values are good

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