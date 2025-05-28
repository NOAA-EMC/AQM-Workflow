#!/usr/bin/env python3

# Python script to handle fire emission (RAVE) to 9-km NA domain

import xarray as xr
from netCDF4 import Dataset
import os
import sys
import argparse
import numpy as np
import ESMF

def RAVE_remake_allspecies(date, cyc, src_map, tgt_map, weight_file, input_fire, output_fire):

    year = date[0:4]
    mm = date[4:6]
    dd = date[6:8]

    ds_in = xr.open_dataset(src_map)
    ds_out = xr.open_dataset(tgt_map)

    src_latt = ds_in['grid_latt']
    src_lont2 = ds_in['grid_lont']
    src_lont = xr.where(src_lont2>0.0,src_lont2,src_lont2+360.0)
    src_lat  = ds_in['grid_lat']
    src_lon  = ds_in['grid_lon']

    tgt_latt = ds_out['grid_latt']
    tgt_lont = ds_out['grid_lont']
    tgt_lat  = ds_out['grid_lat']
    tgt_lon  = ds_out['grid_lon']

    src_shape = src_latt.shape
    tgt_shape = tgt_latt.shape

    srcgrid = ESMF.Grid(np.array(src_shape), staggerloc=[ESMF.StaggerLoc.CENTER, ESMF.StaggerLoc.CORNER],coord_sys=ESMF.CoordSys.SPH_DEG)
    tgtgrid = ESMF.Grid(np.array(tgt_shape), staggerloc=[ESMF.StaggerLoc.CENTER, ESMF.StaggerLoc.CORNER],coord_sys=ESMF.CoordSys.SPH_DEG)

    src_cen_lon = srcgrid.get_coords(0, staggerloc=ESMF.StaggerLoc.CENTER)
    src_cen_lat = srcgrid.get_coords(1, staggerloc=ESMF.StaggerLoc.CENTER)

    tgt_cen_lon = tgtgrid.get_coords(0, staggerloc=ESMF.StaggerLoc.CENTER)
    tgt_cen_lat = tgtgrid.get_coords(1, staggerloc=ESMF.StaggerLoc.CENTER)

    src_cen_lon[...] = src_lont
    src_cen_lat[...] = src_latt

    tgt_cen_lon[...] = tgt_lont
    tgt_cen_lat[...] = tgt_latt

    src_con_lon = srcgrid.get_coords(0, staggerloc=ESMF.StaggerLoc.CORNER)
    src_con_lat = srcgrid.get_coords(1, staggerloc=ESMF.StaggerLoc.CORNER)

    tgt_con_lon = tgtgrid.get_coords(0, staggerloc=ESMF.StaggerLoc.CORNER)
    tgt_con_lat = tgtgrid.get_coords(1, staggerloc=ESMF.StaggerLoc.CORNER)

    src_con_lon[...] = src_lon
    src_con_lat[...] = src_lat

    tgt_con_lon[...] = tgt_lon
    tgt_con_lat[...] = tgt_lat

    ds_togid=xr.open_dataset(input_fire)
    area=ds_togid['area']
    QA=ds_togid['QA']
    tgt_area=ds_out['area']
    #tgt_latt = ds_togid['grid_latt']
    #tgt_lont = ds_togid['grid_lont']
    land_cover = ds_out['land_cover']

    srcfield = ESMF.Field(srcgrid, name='test')
    tgtfield = ESMF.Field(tgtgrid, name='test')

    srcfield.data[...] = QA[0,:,:]

    regridder = ESMF.RegridFromFile(srcfield, tgtfield, weight_file)

    fout=Dataset(output_fire,'w')
    fout.createDimension('Time',24)
    fout.createDimension('xFRP',1152)
    fout.createDimension('yFRP',768)
    
    setattr(fout,'PRODUCT_ALGORITHM_VERSION','Beta')
    setattr(fout,'TIME_RANGE','72 hours')
    setattr(fout,'RangeBeginningDate\(YYYY-MM-DD\)',year+'-'+mm+'-'+dd)
    setattr(fout,'RangeBeginningTime\(UTC-hour\)',cyc)
    setattr(fout,'WestBoundingCoordinate\(degree\)','152.859f')
    setattr(fout,'EastBoundingCoordinate\(degree\)','331.141f')
    setattr(fout,'NorthBoundingCoordinate\(degree\)','81.0247f')
    setattr(fout,'SouthBoundingCoordinate\(degree\)','7.81713f')
    
    Store_latlon_by_Level(fout,'Latitude',tgt_latt,'cell center latitude','degrees_north','2D','-9999.f','1.f')
    Store_latlon_by_Level(fout,'Longitude',tgt_lont,'cell center longitude','degrees_east','2D','-9999.f','1.f')
    Store_latlon_by_Level(fout,'land_cover',land_cover,'land cover type','unitless','2D','-9999.f','1.f')

    hrs=np.linspace(0,23,num=24)
    #print(hrs)

    vars_emis = ["PM25_scaled","CO","VOCs","NOx","BC_scaled","OC_scaled","SO2","NH3","FRP_MEAN"]
    
    for svar in vars_emis:

         #print(svar)

         srcfield = ESMF.Field(srcgrid, name=svar)
         tgtfield = ESMF.Field(tgtgrid, name=svar)

         if svar=='FRP_MEAN':
           Store_by_Level(fout,'MeanFRP','Mean Fire Radiative Power','MW','3D','0.f','1.f')
         elif svar=='PM25_scaled':
           Store_by_Level(fout,'PM2.5',svar+' Biomass Emissions','kg m-2 s-1','3D','0.f','1.f')
         elif svar=='BC_scaled':
           Store_by_Level(fout,'BC','BC Biomass Emissions','kg m-2 s-1','3D','0.f','1.f')
         elif svar=='OC_scaled':
           Store_by_Level(fout,'OC','OC Biomass Emissions','kg m-2 s-1','3D','0.f','1.f')
         else :
           Store_by_Level(fout,svar,svar+' Biomass Emissions','kg m-2 s-1','3D','0.f','1.f')

         src_rate = ds_togid[svar].fillna(0)/area
         src_QA = xr.where(QA>1,src_rate,0.0)#,keep_attrs=True)

         #print(np.sum(src_QA))

         for hr in range(0,24,1):
            #print(hr)
            src_cut = src_QA[hr,:,:]

            srcfield.data[...] = src_cut

            #print('=============before regridding==========='+svar)
            #total_mass=np.sum(src_cut*area)
            #print(total_mass)

            tgtfield = regridder(srcfield, tgtfield)

            if svar=='FRP_MEAN':
              tgt_rate = tgtfield.data*(tgt_area*1.e-6)
              fout.variables['MeanFRP'][hr,:,:] = tgt_rate
              #print('=============after regridding==========='+svar)
              #total_mass=np.sum(tgt_rate)
              #print(total_mass)
            elif svar=='PM25_scaled':
              tgt_rate = tgtfield.data*1.e-6/3600
              fout.variables['PM2.5'][hr,:,:] = tgt_rate
              #print('=============after regridding==========='+svar)
              #total_mass=np.sum(tgt_rate*tgt_area*3600)
              #print(total_mass)
            elif svar=='BC_scaled':
              tgt_rate = tgtfield.data*1.e-6/3600
              fout.variables['BC'][hr,:,:] = tgt_rate
              #print('=============after regridding==========='+svar)
              #total_mass=np.sum(tgt_rate*tgt_area*3600)
              #print(total_mass)
            elif svar=='OC_scaled':
              tgt_rate = tgtfield.data*1.e-6/3600
              fout.variables['OC'][hr,:,:] = tgt_rate
              #print('=============after regridding==========='+svar)
              #total_mass=np.sum(tgt_rate*tgt_area*3600)
              #print(total_mass)
            else:
              tgt_rate = tgtfield.data*1.e-6/3600
              fout.variables[svar][hr,:,:] = tgt_rate
              #print('=============after regridding==========='+svar)
              #total_mass=np.sum(tgt_rate*tgt_area*3600)
              #print(total_mass)
    
    fout.close()


def Store_time_by_Level(fout,varname,var,long_name,yr,mm,dd,cyc,DATE1):
    if varname=='time':
        var_out = fout.createVariable(varname, 'f4', ('Time',))
        var_out.long_name = long_name
        var_out.standard_name = long_name
        fout.variables[varname][:]=var
        var_out.units = 'hours since '+yr+'-'+mm+'-'+dd+' '+cyc+':00:00'
        var_out.calendar = 'gregorian'
        var_out.axis='T'
        var_out.time_increment='010000'
        var_out.begin_date=DATE1
        var_out.begin_time='060000'


def Store_latlon_by_Level(fout,varname,var,long_name,units,dim,fval,sfactor):
    if dim=='2D':
        var_out = fout.createVariable(varname,   'f4', ('yFRP','xFRP'))
        var_out.units=units
        var_out.long_name=long_name
        var_out.standard_name=varname
        fout.variables[varname][:]=var
        var_out.FillValue=fval
        var_out.coordinates='Latitude Longitude'


def Store_by_Level(fout,varname,long_name,units,dim,fval,sfactor):
    if dim=='3D':
        var_out = fout.createVariable(varname,   'f4', ('Time','yFRP','xFRP'))
        var_out.units=units
        var_out.long_name = long_name
        var_out.standard_name=long_name
        var_out.FillValue=fval
        var_out.coordinates='Time Latitude Longitude'


def parse_args(argv):

    parser = argparse.ArgumentParser(
        description='Handle fire emission data.'
    )

    parser.add_argument('-d', '--date',
                        dest="date",
                        required=True,
                        help='Date for regridding.',
                        )
    parser.add_argument('-c', '--cyc',
                        dest="cyc",
                        required=True,
                        help='Cycle hour.',
                        )
    parser.add_argument('-s', '--src_map',
                        dest="src_map",
                        required=True,
                        help='source map.',
                        )
    parser.add_argument('-t', '--tgt_map',
                        dest="tgt_map",
                        required=True,
                        help='target map.',
                        )
    parser.add_argument('-w', '--weight_file',
                        dest="weight_file",
                        required=True,
                        help='weight file.',
                        )
    parser.add_argument('-i', '--input_fire',
                        dest="input_fire",
                        required=True,
                        help='Path to the RAVE fire data file.',
                        )
    parser.add_argument('-o', '--output_fire',
                        dest="output_fire",
                        required=True,
                        help='Path to the output data file.',
                        )
    return parser.parse_args(argv)


# Main call =====================================================
if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    RAVE_remake_allspecies(
        date=args.date,
        cyc=args.cyc,
        src_map=args.src_map,
        tgt_map=args.tgt_map,
        weight_file=args.weight_file,
        input_fire=args.input_fire,
        output_fire=args.output_fire
    )

