#This is a Python file to make aqm_cycled.def a Python file
#This file is specific to each platform

#imports
import ecflow as ecf

#Example from Defs API version 2
#Loop through forecast hours 
#f_ = family, tsk_ = task, trg_ = trigger
defs = Defs()
suite = defs.add_suite('nco_aqm')
f_primary = suite.add_family('f_primary')
defs.suite.f_primary += [Edit(aqm_ver='v8.0'), 
                         Edit(PACKAGEHOME='/lfs/h2/emc/physics/noscrub/%EMC_USER%/nwdev/packages/aqm.%aqm_ver%'),
                         Edit(NET='aqm'),
                         Edit(RUN='aqm'),
                         Edit(PROJ='aqm'),
                         Edit(PROJENV='AQM'),
                         Edit(MACHINE_SITE='development'),
                         Edit(ENVIR='dev'),
                         Edit(QUEUE='devhigh'),
                         Edit(QUEUE_ARCH='dev_transfer'),
                         Edit(OUTPUTDIR='/lfs/h2/emc/ptmp/%EMC_USER%/ecflow_aqm/para/output/prod/today')] 
f_00 = f_primary.add_family('00')
f_00 += [Edit(CYC='00')]
f_00 += [Task('cycle_end',
         Edit(ECF_FILES='%PACKAGEHOME%/ecf'),
         cron = CRON('23:00'))]
f_aqm = f_00.add_family('f_aqm')
#f_v1 is the Python variable for family f_v1.0
f_v1 = f_aqm.add_family('f_v1.0') 
f_v1 += [Edit(ECF_FILES='%PACKAGEHOME%/ecf')]

#Nexus
f_nexus = f_v1.add_family('f_nexus')
f_nexus += [Task('jaqm_nexus_emission_00',
             Edit(NSPT = '00'),
             Trigger('TIME >= 0142 and TIME < 0742'))]
f_nexus += [Task('jaqm_nexus_emission_01',
             Edit(NSPT = '01'),
             Trigger('TIME >= 0142 and TIME < 0742'))]
f_nexus += [Task('jaqm_nexus_emission_02',
             Edit(NSPT = '02'),
             Trigger('TIME >= 0142 and TIME < 0742'))]
f_nexus += [Task('jaqm_nexus_emission_03',
             Edit(NSPT = '03'),
             Trigger('TIME >= 0142 and TIME < 0742'))]
f_nexus += [Task('jaqm_nexus_emission_04',
             Edit(NSPT = '04'),
             Trigger('TIME >= 0142 and TIME < 0742'))]
f_nexus += [Task('jaqm_nexus_emission_05',
             Edit(NSPT = '05'),
             Trigger('TIME >= 0142 and TIME < 0742'))]
f_nexus += [Task('jaqm_nexus_post_split',
             Trigger('./jaqm_nexus_emission_00==complete' and
                        './jaqm_nexus_emission_01==complete' and
                        './jaqm_nexus_emission_02==complete' and
                        './jaqm_nexus_emission_03==complete' and
                        './jaqm_nexus_emission_04==complete' and
                        './jaqm_nexus_emission_05==complete'))]
#Nexus as loop initial------------------------------------------------
f_nexus = f_v1.add_family('f_nexus')
for i in range(5):
    f_nexus += [Task('jaqm_nexus_emission_0'+str(i),
                Edit(NSPT = '0'+str(i)),
                Trigger('TIME >= 0142 and TIME < 0742'))]
f_nexus += [Task('jaqm_nexus_post_split',
             Trigger('./jaqm_nexus_emission_00==complete' and
                        './jaqm_nexus_emission_01==complete' and
                        './jaqm_nexus_emission_02==complete' and
                        './jaqm_nexus_emission_03==complete' and
                        './jaqm_nexus_emission_04==complete' and
                        './jaqm_nexus_emission_05==complete'))]
#-------------------------------------------------------------------------

#Prep ICs and LBCs
f_prep = f_aqm.add_family('f_prep')
f_prep += [Task('jaqm_make_ics',
            Trigger('TIME >= 0142 and TIME < 0742'))]
f_prep += [Task('jaqm_make_lbcs',
            Trigger('TIME >= 0142 and TIME < 0742'))]
f_prep += [Task('jaqm_ics',
            Trigger('./jaqm_make_ics==complete'))]
f_prep += [Task('jaqm_lbcs',
            Trigger('./jaqm_make_lbcs==complete' and './jaqm_make_ics==complete'))]

#Point Source Fire Emissions
f_pts_fire_emis = f_aqm.add_family('f_pts_fire_emis')
f_pts_fire_emis += [Task('jaqm_point_source',
                    Trigger('TIME >= 0142 and TIME < 0742'))] 
f_pts_fire_emis += [Task('jaqm_fire_emission',
                    Trigger('TIME >= 0142 and TIME < 0742'))]

#Forecast 
f_forecast = f_aqm.add_family('f_forecast')
f_forecast += [Task('jaqm_forecast',
                Trigger('../nexus==complete' and '../prep==complete' and '../pts_fire_emis==complete'),
                Event(1, 'release_manager'))] 
f_forecast += [Task('jaqm_forecast_manager',
                Trigger('./jaqm_forecast:release_manager'),
                Event(1, 'restart_gp1_rdy'),
                Event(2, '000_rdy'),
                Event(3, '001_rdy'),
                Event(4, '002_rdy'),
                Event(5, '003_rdy'),
                Event(6, '004_rdy'),
                Event(7, '005_rdy'),
                Event(8, '006_rdy'),)]
#forecast as loop--------------------------------------------------------------
f_forecast = f_aqm.add_family('f_forecast')
f_forecast += [Task('jaqm_forecast',
                Trigger('../nexus==complete' and '../prep==complete' and '../pts_fire_emis==complete'),
                Event(1, 'release_manager'))] 
for i in range(1,8):
    if i == 1:
        f_forecast += [Task('jaqm_forecast_manager',
                        Trigger('./jaqm_forecast:release_manager'),
                        Event(i, 'restart_gp1_rdy'))]
    else:                
        f_forecast += [Task('jaqm_forecast_manager',
                        Trigger('./jaqm_forecast:release_manager'),
                        Event(i, '00'+ str(i-2)+'0_rdy'),)]
# ----------------------------------------------------------------------------- 

#Post
f_post = f_aqm.add_family('f_post')
f_post += [Task('jaqm_post_f000',
             Edit(FHR = '000'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f001',
             Edit(FHR = '001'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f002',
             Edit(FHR = '002'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f003',
             Edit(FHR = '003'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f004',
             Edit(FHR = '004'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f005',
             Edit(FHR = '005'),
             Trigger('../forecast==complete'))]
#Post as loop---------------------------------------------------------------
f_post = f_aqm.add_family('f_post')
for i in range(6):
    f_post += [Task('jaqm_post_f00'+str(i),
                Edit(FHR = '00'+str(i)),
                Trigger('../forecast==complete'))]
#---------------------------------------------------------------------------

#Product
f_product = f_aqm.add_family('f_product')
f_product += [Task('jaqm_pre_post_stat',
                Trigger('../forecast==complete'))]
f_product += [Task('jaqm_post_stat_o3',
                Trigger('./jaqm_pre_post_stat==complete'))]
f_product += [Task('jaqm_post_stat_pm25',
                Trigger('./jaqm_pre_post_stat==complete'))]
f_product += [Task('jaqm_bias_correction_o3',
                Trigger('./jaqm_pre_post_stat==complete'))]
f_product += [Task('jaqm_bias_correction_pm25',
                Trigger('./jaqm_pre_post_stat==complete'))]

#06 Cycle
f_06 = f_primary.add_family('06')
f_06 += [Edit(CYC='06')]
f_06 += [Task('cycle_end',
         Edit(ECF_FILES='%PACKAGEHOME%/ecf'),
         cron = CRON('05:00'))]
f_aqm = f_06.add_family(f_aqm)
f_v1 = f_aqm.add_family('f_v1.0')
f_v1 += [Edit(ECF_FILES='%PACKAGEHOME%/ecf')]

#Nexus
f_nexus = f_v1.add_family('f_nexus')
f_nexus += [Task('jaqm_nexus_emission_00',
             Edit(NSPT = '00'),
             Trigger('TIME >= 0742 and :TIME < 1342'))]
f_nexus += [Task('jaqm_nexus_emission_01',
             Edit(NSPT = '01'),
             Trigger('TIME >= 0742 and :TIME < 1342'))]
f_nexus += [Task('jaqm_nexus_emission_02',
             Edit(NSPT = '02'),
             Trigger('TIME >= 0742 and :TIME < 1342'))]
f_nexus += [Task('jaqm_nexus_emission_03',
             Edit(NSPT = '03'),
             Trigger('TIME >= 0742 and :TIME < 1342'))]
f_nexus += [Task('jaqm_nexus_emission_04',
             Edit(NSPT = '04'),
             Trigger('TIME >= 0742 and :TIME < 1342'))]
f_nexus += [Task('jaqm_nexus_emission_05',
             Edit(NSPT = '05'),
             Trigger('TIME >= 0742 and :TIME < 1342'))]
f_nexus += [Task('jaqm_nexus_post_split',
             Trigger('./jaqm_nexus_emission_00==complete' and
                        './jaqm_nexus_emission_01==complete' and
                        './jaqm_nexus_emission_02==complete' and
                        './jaqm_nexus_emission_03==complete' and
                        './jaqm_nexus_emission_04==complete' and
                        './jaqm_nexus_emission_05==complete'))]
#Nexus as loop for first 6 hours -------------------------------------
f_nexus = f_v1.add_family('f_nexus')
for i in range(5):
    f_nexus += [Task('jaqm_nexus_emission_0'+str(i),
                Edit(NSPT = '0'+str(i)),
                Trigger('TIME >= 0742 and :TIME < 1342'))]
f_nexus += [Task('jaqm_nexus_post_split',
             Trigger('./jaqm_nexus_emission_00==complete' and
                        './jaqm_nexus_emission_01==complete' and
                        './jaqm_nexus_emission_02==complete' and
                        './jaqm_nexus_emission_03==complete' and
                        './jaqm_nexus_emission_04==complete' and
                        './jaqm_nexus_emission_05==complete'))]
#-------------------------------------------------------------------------

#Prep ICs and LBCs
f_prep = f_v1.add_family('f_prep')
f_prep += [Task('jaqm_make_ics',
            Trigger('TIME >= 0742 and :TIME < 1342'))]
f_prep += [Task('jaqm_make_lbcs',
            Trigger('TIME >= 0742 and :TIME < 1342'))]
f_prep += [Task('jaqm_ics',
            Trigger('./jaqm_make_ics==complete'))]
f_prep += [Task('jaqm_lbcs',
            Trigger('./jaqm_make_lbcs==complete' and './jaqm_make_ics==complete'))]

#Point Source Fire Emissions
f_pts_fire_emis = f_v1.add_family('f_pts_fire_emis')
f_pts_fire_emis += [Task('jaqm_point_source',
                    Trigger('TIME >= 0742 and :TIME < 1342'))] 
f_pts_fire_emis += [Task('jaqm_fire_emission',
                    Trigger('TIME >= 0742 and :TIME < 1342'))]

#Forecast
f_forecast = f_v1.add_family('f_forecast')
f_forecast += [Task('jaqm_forecast',
                Trigger('../nexus==complete' and '../prep==complete' and '../pts_fire_emis==complete'),
                Event(1, 'release_manager'))] 
f_forecast += [Task('jaqm_forecast_manager',
                Trigger('./jaqm_forecast:release_manager'),
                Event(1, 'restart_gp1_rdy'),
                Event(2, 'restart_gp2_rdy'),
                Event(3, 'restart_gp3_rdy'),
                Event(4, 'restart_gp4_rdy'),
                Event(5, 'restart_gp5_rdy'),
                Event(6, 'restart_gp6_rdy'),
                Event(7, 'restart_gp7_rdy'),
                Event(8, 'restart_gp8_rdy'),
                Event(9, 'restart_gp9_rdy'),
                Event(10, 'restart_gp10_rdy'),
                Event(11, 'restart_gp11_rdy'),
                Event(12, '000_rdy'),
                Event(13, '001_rdy'),
                Event(14, '002_rdy'),
                Event(15, '003_rdy'),
                Event(16, '004_rdy'),
                Event(17, '005_rdy'),
                Event(18, '006_rdy'),
                Event(19, '007_rdy'),
                Event(20, '008_rdy'),
                Event(21, '009_rdy'),
                Event(22, '010_rdy'),
                Event(23, '011_rdy'),
                Event(24, '012_rdy'),
                Event(25, '013_rdy'),
                Event(26, '014_rdy'),
                Event(27, '015_rdy'),
                Event(28, '016_rdy'),
                Event(29, '017_rdy'),
                Event(30, '018_rdy'),
                Event(31, '019_rdy'),
                Event(32, '020_rdy'),
                Event(33, '021_rdy'),
                Event(34, '022_rdy'),
                Event(35, '023_rdy'),
                Event(36, '024_rdy'),
                Event(37, '025_rdy'),
                Event(38, '026_rdy'),
                Event(39, '027_rdy'),
                Event(40, '028_rdy'),
                Event(41, '029_rdy'),
                Event(42, '030_rdy'),
                Event(43, '031_rdy'),
                Event(44, '032_rdy'),
                Event(45, '033_rdy'),
                Event(46, '034_rdy'),
                Event(47, '035_rdy'),
                Event(48, '036_rdy'),
                Event(49, '037_rdy'),
                Event(50, '038_rdy'),
                Event(51, '039_rdy'),
                Event(52, '040_rdy'),
                Event(53, '041_rdy'),
                Event(54, '042_rdy'),
                Event(55, '043_rdy'),
                Event(56, '044_rdy'),
                Event(57, '045_rdy'), 
                Event(58, '046_rdy'), 
                Event(59, '047_rdy'), 
                Event(60, '048_rdy'), 
                Event(61, '049_rdy'), 
                Event(62, '050_rdy'), 
                Event(63, '051_rdy'), 
                Event(64, '052_rdy'), 
                Event(65, '053_rdy'),
                Event(66, '054_rdy'), 
                Event(67, '055_rdy'), 
                Event(68, '056_rdy'), 
                Event(69, '057_rdy'), 
                Event(70, '058_rdy'), 
                Event(71, '059_rdy'), 
                Event(72, '060_rdy'), 
                Event(73, '061_rdy'), 
                Event(74, '062_rdy'),
                Event(75, '063_rdy'), 
                Event(76, '064_rdy'), 
                Event(77, '065_rdy'), 
                Event(78, '066_rdy'), 
                Event(79, '067_rdy'), 
                Event(80, '068_rdy'),
                Event(81, '069_rdy'),  
                Event(82, '070_rdy'),  
                Event(83, '071_rdy'),  
                Event(84, '072_rdy'),)]
#forecast as loop--------------------------------------------------------------
f_forecast = f_v1.add_family('f_forecast')
f_forecast += [Task('jaqm_forecast',
                Trigger('../nexus==complete' and '../prep==complete' and '../pts_fire_emis==complete'),
                Event(1, 'release_manager'))]
for i in range(1,84):
    if 1 <= i <= 11:
        f_forecast += [Task('jaqm_forecast_manager',
                        Trigger('./jaqm_forecast:release_manager'),
                        Event(i, 'restart_gp'+str(i)+'1_rdy'))]
    else:
        f_forecast += [Task('jaqm_forecast_manager',
                        Trigger('./jaqm_forecast:release_manager'),
                Event(i, '0'+str(i-12)+'_rdy'))]
# -----------------------------------------------------------------------------  

#Post
f_post = f_v1.add_family('f_post')
f_post += [Task('jaqm_post_f000',
             Edit(FHR = '000'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f001',
             Edit(FHR = '001'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f002',
             Edit(FHR = '002'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f003',
             Edit(FHR = '003'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f004',
             Edit(FHR = '004'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f005',
             Edit(FHR = '005'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f006',
             Edit(FHR = '006'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f007',
             Edit(FHR = '007'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f008',
             Edit(FHR = '008'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f009',
             Edit(FHR = '009'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f010',
             Edit(FHR = '010'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f011',
             Edit(FHR = '011'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f012',
             Edit(FHR = '012'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f013',
             Edit(FHR = '013'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f014',
             Edit(FHR = '014'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f015',
             Edit(FHR = '015'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f016',
             Edit(FHR = '016'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f017',
             Edit(FHR = '017'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f018',
             Edit(FHR = '018'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f019',
             Edit(FHR = '019'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f020',
             Edit(FHR = '020'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f021',
             Edit(FHR = '021'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f022',
             Edit(FHR = '022'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f023',
             Edit(FHR = '023'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f024',
             Edit(FHR = '024'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f025',
             Edit(FHR = '025'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f026',
             Edit(FHR = '026'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f027',
             Edit(FHR = '027'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f028',
             Edit(FHR = '028'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f029',
             Edit(FHR = '029'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f030',
             Edit(FHR = '030'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f031',
             Edit(FHR = '031'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f032',
             Edit(FHR = '032'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f033',
             Edit(FHR = '033'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f034',
             Edit(FHR = '034'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f035',
             Edit(FHR = '035'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f036',
             Edit(FHR = '036'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f037',
             Edit(FHR = '037'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f038',
             Edit(FHR = '038'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f039',
             Edit(FHR = '039'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f040',
             Edit(FHR = '040'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f041',
             Edit(FHR = '041'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f042',
             Edit(FHR = '042'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f043',
             Edit(FHR = '043'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f044',
             Edit(FHR = '044'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f045',
             Edit(FHR = '045'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f046',
             Edit(FHR = '046'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f047',
             Edit(FHR = '047'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f048',
             Edit(FHR = '048'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f049',
             Edit(FHR = '049'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f050',
             Edit(FHR = '050'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f051',
             Edit(FHR = '051'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f052',
             Edit(FHR = '052'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f053',
             Edit(FHR = '053'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f054',
             Edit(FHR = '054'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f055',
             Edit(FHR = '055'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f056',
             Edit(FHR = '056'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f057',
             Edit(FHR = '057'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f058',
             Edit(FHR = '058'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f059',
             Edit(FHR = '059'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f060',
             Edit(FHR = '060'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f061',
             Edit(FHR = '061'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f062',
             Edit(FHR = '062'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f063',
             Edit(FHR = '063'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f064',
             Edit(FHR = '064'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f065',
             Edit(FHR = '065'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f066',
             Edit(FHR = '066'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f067',
             Edit(FHR = '067'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f068',
             Edit(FHR = '068'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f069',
             Edit(FHR = '069'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f070',
             Edit(FHR = '070'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f071',
             Edit(FHR = '071'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f072',
             Edit(FHR = '072'),
             Trigger('../forecast==complete'))]
#Post as loop---------------------------------------------------------------
f_post = f_aqm.add_family('f_post')
for i in range(71):
    if i <= 9: 
        f_post += [Task('jaqm_post_f00'+str(i),
                    Edit(FHR = '00'+str(i)),
                    Trigger('../forecast==complete'))]
    else: 
                f_post += [Task('jaqm_post_f0'+str(i),
                    Edit(FHR = '0'+str(i)),
                    Trigger('../forecast==complete'))]
#---------------------------------------------------------------------------

#Product
f_product = f_v1.add_family('f_product')
f_product += [Task('jaqm_pre_post_stat',
                Trigger('../forecast==complete'))]
f_product += [Task('jaqm_post_stat_o3',
                Trigger('./jaqm_pre_post_stat==complete'))]
f_product += [Task('jaqm_post_stat_pm25',
                Trigger('./jaqm_pre_post_stat==complete'))]
f_product += [Task('jaqm_bias_correction_o3',
                Trigger('./jaqm_pre_post_stat==complete'))]
f_product += [Task('jaqm_bias_correction_pm25',
                Trigger('./jaqm_pre_post_stat==complete'))]

#18 Cycle
f_18 = f_primary.add_family('18')
f_18 += [Edit(CYC='18')]
f_18 += [Task('cycle_end',
         Edit(ECF_FILES='%PACKAGEHOME%/ecf'),
         cron = CRON('17:00'))]
f_aqm = f_018.add_family(f_aqm)
f_v1 = f_aqm.add_family('f_v1.0')
f_v1 += [Edit(ECF_FILES='%PACKAGEHOME%/ecf')]

#Nexus
f_nexus = f_v1.add_family('f_nexus')
f_nexus += [Task('jaqm_nexus_emission_00',
             Edit(NSPT = '00'),
             Trigger('TIME >= 1942 and :TIME < 2342'))]
f_nexus += [Task('jaqm_nexus_emission_01',
             Edit(NSPT = '01'),
             Trigger('TIME >= 1942 and :TIME < 2342'))]
f_nexus += [Task('jaqm_nexus_emission_02',
             Edit(NSPT = '02'),
             Trigger('TIME >= 1942 and :TIME < 2342'))]
f_nexus += [Task('jaqm_nexus_emission_03',
             Edit(NSPT = '03'),
             Trigger('TIME >= 1942 and :TIME < 2342'))]
f_nexus += [Task('jaqm_nexus_emission_04',
             Edit(NSPT = '04'),
             Trigger('TIME >= 1942 and :TIME < 2342'))]
f_nexus += [Task('jaqm_nexus_emission_05',
             Edit(NSPT = '05'),
             Trigger('TIME >= 1942 and :TIME < 2342'))]
f_nexus += [Task('jaqm_nexus_post_split',
             Trigger('./jaqm_nexus_emission_00==complete' and
                        './jaqm_nexus_emission_01==complete' and
                        './jaqm_nexus_emission_02==complete' and
                        './jaqm_nexus_emission_03==complete' and
                        './jaqm_nexus_emission_04==complete' and
                        './jaqm_nexus_emission_05==complete'))]
#Nexus as loop---------------------------------------------------------
f_nexus = f_v1.add_family('f_nexus')
for i in range(5):
    f_nexus += [Task('jaqm_nexus_emission_0'+str(i),
                Edit(NSPT = '0'+str(i)),
                Trigger('TIME >= 1942 and :TIME < 2342'))]
f_nexus += [Task('jaqm_nexus_post_split',
             Trigger('./jaqm_nexus_emission_00==complete' and
                        './jaqm_nexus_emission_01==complete' and
                        './jaqm_nexus_emission_02==complete' and
                        './jaqm_nexus_emission_03==complete' and
                        './jaqm_nexus_emission_04==complete' and
                        './jaqm_nexus_emission_05==complete'))]
#-------------------------------------------------------------------------

#Prep
f_prep = f_v1.add_family('f_prep')
f_prep += [Task('jaqm_make_ics',
            Trigger('TIME >= 1942 and :TIME < 2342'))]
f_prep += [Task('jaqm_make_lbcs',
            Trigger('TIME >= 1942 and :TIME < 2342'))]
f_prep += [Task('jaqm_ics',
            Trigger('./jaqm_make_ics==complete'))]
f_prep += [Task('jaqm_lbcs',
            Trigger('./jaqm_make_lbcs==complete' and './jaqm_make_ics==complete'))]

#Point Source Fire Emissions
f_pts_fire_emis = f_v1.add_family('f_pts_fire_emis')
f_pts_fire_emis += [Task('jaqm_point_source',
                    Trigger('TIME >= 1942 and :TIME < 2342'))] 
f_pts_fire_emis += [Task('jaqm_fire_emission',
                    Trigger('TIME >= 1942 and :TIME < 2342'))]

#Forecast
f_forecast = f_v1.add_family('f_forecast')
f_forecast += [Task('jaqm_forecast',
                Trigger('../nexus==complete' and '../prep==complete' and '../pts_fire_emis==complete'),
                Event(1, 'release_manager'))] 
f_forecast += [Task('jaqm_forecast_manager',
                Trigger('./jaqm_forecast:release_manager'),
                Event(1, 'restart_gp1_rdy'),
                Event(2, '000_rdy'),
                Event(3, '001_rdy'),
                Event(4, '002_rdy'),
                Event(5, '003_rdy'),
                Event(6, '004_rdy'),
                Event(7, '005_rdy'),
                Event(8, '006_rdy'))]
#forecast as loop--------------------------------------------------------------
f_forecast = f_v1.add_family('f_forecast')
f_forecast += [Task('jaqm_forecast',
                Trigger('../nexus==complete' and '../prep==complete' and '../pts_fire_emis==complete'),
                Event(1, 'release_manager'))]  
for i in range(1,8):
    if i == 1:
        f_forecast += [Task('jaqm_forecast_manager',
                        Trigger('./jaqm_forecast:release_manager'),
                        Event(i, 'restart_gp1_rdy'))]
    else:                
        f_forecast += [Task('jaqm_forecast_manager',
                        Trigger('./jaqm_forecast:release_manager'),
                        Event(i, '00'+ str(i-2)+'0_rdy'),)]
# -----------------------------------------------------------------------------

#Post
f_post = f_v1.add_family('f_post')
f_post += [Task('jaqm_post_f000',
             Edit(FHR = '000'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f001',
             Edit(FHR = '001'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f002',
             Edit(FHR = '002'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f003',
             Edit(FHR = '003'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f004',
             Edit(FHR = '004'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f005',
             Edit(FHR = '005'),
             Trigger('../forecast==complete'))]
f_post += [Task('jaqm_post_f006',
             Edit(FHR = '006'))]
#Post as loop---------------------------------------------------------------
f_post = f_aqm.add_family('f_post')
for i in range(7):
    f_post += [Task('jaqm_post_f00'+str(i),
                Edit(FHR = '00'+str(i)),
                Trigger('../forecast==complete'))]
#---------------------------------------------------------------------------

#Product
f_product = f_v1.add_family('f_product')
f_product += [Task('jaqm_pre_post_stat',
                Trigger('../forecast==complete'))]
f_product += [Task('jaqm_post_stat_o3',
                Trigger('./jaqm_pre_post_stat==complete'))]
f_product += [Task('jaqm_post_stat_pm25',
                Trigger('./jaqm_pre_post_stat==complete'))]
f_product += [Task('jaqm_bias_correction_o3',
                Trigger('./jaqm_pre_post_stat==complete'))]
f_product += [Task('jaqm_bias_correction_pm25',
                Trigger('./jaqm_pre_post_stat==complete'))]

defs.save_as_defs('test_file.def')  # save defs into file