#This is a Python file to generate aqm_cycled.def
#as 6hr dev testing with machine & user configurability

#imports
import ecflow as ecf

#variables

#main function to bring in all other functions
#creates def, suite, and primary family 
#f_ = family
def main():
    defs = ecf.Defs()
    includes(defs) 
    cycle_00(defs)
    nexus(defs)
    prep(defs)
    pts_fire_emis(defs)
    forecast(defs)
    post(defs)
    product(defs)
    out_file(defs)

#user includes
def includes(defs):
    suite = defs.add_suite('nco_aqm') 
    f_primary = suite.add_family('primary')
    defs.nco_aqm.primary += [ ecf.Edit(aqm_ver='v8.0.1'),
                    ecf.Edit(PACKAGEHOME = '/lfs/h2/emc/physics/noscrub/%EMC_USER%/nwdev/packages/aqm.%aqm_ver%'),
                    ecf.Edit(NET = 'aqm'),
                    ecf.Edit(RUN = 'aqm'),
                    ecf.Edit(PROJ='AQM'),
                    ecf.Edit(PROJENV='DEV'),
                    ecf.Edit(MACHINE_SITE='development'),
                    ecf.Edit(ENVIR='dev'),
                    ecf.Edit(QUEUE='devhigh'),
                    ecf.Edit(QUEUE_ARCH='dev_transfer'),
                    ecf.Edit(OUTPUTDIR='/lfs/h2/emc/ptmp/%EMC_USER%/ecflow_aqm/para/output/prod/today')] 
    print('primary family finished')
    print('defs finished')
    out_file(defs)

#creates 00 Cycle------------------------------------------------
def cycle_00(defs):
    f_00 = defs.nco_aqm.primary.add_family('C00') #00
    f_00 += [ecf.Edit(CYC='00')]
    #tsk is task 
    tsk_cycle_end = f_00.add_task('cycle_end')
    tsk_cycle_end += [ecf.Edit(ECF_FILES='%PACKAGEHOME%/ecf'),
                        ecf.Cron('23:00')]
    f_aqm = f_00.add_family('aqm') #aqm
    #f_v1 is the Python variable for family f_v1.0
    f_v1 = f_aqm.add_family('v1_0')  #v1.0
    f_v1 += [ecf.Edit(ECF_FILES='%PACKAGEHOME%/ecf')]
    print('family 00 finished')
    out_file(defs)

#Nexus------------------------------------------------------------
def nexus(defs):
    f_nexus = defs.nco_aqm.primary.C00.aqm.v1_0.add_family('nexus')  
    for i in range(6):
        tsk_jaqm_nex_emis = f_nexus.add_task('jaqm_nexus_emission_0'+str(i))
        tsk_jaqm_nex_emis += [ecf.Edit(NSPT = '0'+str(i))]
        tsk_jaqm_nex_emis += [ecf.Trigger('TIME >= 0142 and TIME < 0742')]

    f_nexus += [ecf.Task('jaqm_nexus_post_split',
                ecf.Trigger("""./jaqm_nexus_emission_00==complete and ./jaqm_nexus_emission_01==complete and ./jaqm_nexus_emission_02==complete and 
./jaqm_nexus_emission_03==complete and./jaqm_nexus_emission_04==complete and ./jaqm_nexus_emission_05==complete"""))]
    print('nexus finished')
    out_file(defs)
#def out_file(defs):
#    defs.save_as_defs('./test_file_loop.def')  # save defs into file
#    print('test file written')

#Prep ICs and LBCs-----------------------------------------------
def prep(defs):
    f_prep = defs.nco_aqm.primary.C00.aqm.v1_0.add_family('prep')
    f_prep += [ecf.Task('jaqm_make_ics',
                ecf.Trigger('TIME >= 0142 and TIME < 0742'))]
    f_prep += [ecf.Task('jaqm_make_lbcs',
                ecf.Trigger('TIME >= 0142 and TIME < 0742'))]
    f_prep += [ecf.Task('jaqm_ics',
                ecf.Trigger('./jaqm_make_ics==complete'))]
    f_prep += [ecf.Task('jaqm_lbcs',
                ecf.Trigger('./jaqm_make_lbcs==complete and ./jaqm_make_ics==complete'))]
    print('prep finished')
    out_file(defs)

#Point Source Fire Emissions------------------------------------
def pts_fire_emis(defs):
    f_pts_fire_emis = defs.nco_aqm.primary.C00.aqm.v1_0.add_family('f_pts_fire_emis')
    f_pts_fire_emis += [ecf.Task('jaqm_point_source',
                        ecf.Trigger('TIME >= 0142 and TIME < 0742'))] 
    f_pts_fire_emis += [ecf.Task('jaqm_fire_emission',
                        ecf.Trigger('TIME >= 0142 and TIME < 0742'))]
    print('pts fir emis finished')
    out_file(defs)
#def out_file(defs):
#    defs.save_as_defs('./test_file.def')  # save defs into file
#    print('test file written')

#Forecast--------------------------------------------------------
def forecast(defs):
    f_forecast = defs.nco_aqm.primary.C00.aqm.v1_0.add_family('forecast')
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
    out_file(defs)    
    print('forecast finished')
#def out_file(defs):
#    defs.save_as_defs('./test_file_loop.def')  # save defs into file
#    print('test file written')

#defs-----------------------------------------------------------------------
def post(defs):
    f_post = defs.nco_aqm.primary.C00.aqm.v1_0.add_family('post')

    for i in range(7):
        f_post += [ecf.Task('jaqm_post_f00'+str(i),
                    ecf.Edit(FHR = '00'+str(i)),
                    ecf.Trigger('../forecast==complete'))]
    out_file(defs)
    print('post finished')
#def out_file(defs):
#    defs.save_as_defs('./test_file_loop.def')  # save defs into file
#    print('test file written')

#Product--------------------------------------------------------------------
def product(defs):
    f_product = defs.nco_aqm.primary.C00.aqm.v1_0.add_family('product')
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
    out_file(defs)
    print('product finished')

def out_file(defs):
    defs.save_as_defs('./test_file_v2.def')  # save defs into file
    print('test file written')


main()