#!/usr/bin/env python3

# Python script to regrid 3-km GBBEPx fire emission (RAVE) to 13-km RRFS-CMAQ domain

import xarray as xr
from netCDF4 import Dataset
import ESMF
import os
import sys
import argparse
import numpy as np

def parse_args(argv):

    parser = argparse.ArgumentParser(
        description='Regrid fire emission data.'
    )

    parser.add_argument('-d', '--date',
                        help='Date for regridding.',
                        )
    parser.add_argument('-c', '--cycle',
                        help='Cycle hour.',
                        )
    parser.add_argument('-s', '--source',
                        help='Path to the source data file.',
                        )
    parser.add_argument('-o', '--output',
                        help='Path to the output data file.',
                        )
    parser.add_argument('-w', '--weight',
                        help='Path to the regridding weight file.',
                        )
    parser.add_argument('-sg', '--source_grid',
                        help='Path to the source grid file.',
                        )
    parser.add_argument('-tg', '--target_grid',
                        help='Path to the target grid file.',
                        )
    return parser.parse_args(argv)


def intpl_ESMPy_QC_allspecies(argv):

    # parse args
    cla = parse_args(argv)
   
    DATE=cla.date
    cyc=cla.cycle
    weightfile=cla.weight
    ravefire=cla.source
    outfire24h=cla.output
    source_grid_spec=cla.source_grid
    target_grid_spec=cla.target_grid

    year = DATE[0:4]
    mm = DATE[4:6]
    dd = DATE[6:8]

    # source RAW emission grid file
    ds_in = xr.open_dataset(source_grid_spec)
    # target grid file
    ds_out = xr.open_dataset(target_grid_spec)
    # source RAW emission file
    ds_togid = xr.open_dataset(ravefire)

    src_latt = ds_in['grid_latt']
    src_lont = ds_in['grid_lont']
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

    area=ds_togid['area']
    QA=ds_togid['QA']
    tgt_area=ds_out['area']

    srcfield = ESMF.Field(srcgrid, name='test')
    tgtfield = ESMF.Field(tgtgrid, name='test')

    regridder = ESMF.RegridFromFile(srcfield, tgtfield,weightfile)

    # output file
    fout=Dataset(outfire24h,'w')
    fout.createDimension('Time',24)
    fout.createDimension('xFRP',396)
    fout.createDimension('yFRP',232)

    setattr(fout,'PRODUCT_ALGORITHM_VERSION','Beta')
    setattr(fout,'TIME_RANGE','72 hours')
    setattr(fout,'RangeBeginningDate\(YYYY-MM-DD\)',year+'-'+mm+'-'+dd)
    setattr(fout,'RangeBeginningTime\(UTC-hour\)',cyc)
    setattr(fout,'WestBoundingCoordinate\(degree\)','227.506f')
    setattr(fout,'EastBoundingCoordinate\(degree\)','297.434f')
    setattr(fout,'NorthBoundingCoordinate\(degree\)','52.058f')
    setattr(fout,'SouthBoundingCoordinate\(degree\)','22.136f')

    hrs=np.linspace(0,23,num=24)

    Store_latlon_by_Level(fout,'Latitude',tgt_latt,'cell center latitude','degrees_north','2D','-9999.f','1.f')
    Store_latlon_by_Level(fout,'Longitude',tgt_lont,'cell center longitude','degrees_east','2D','-9999.f','1.f')

    vars_emis = ["PM2.5","CO","VOCs","NOx","BC","OC","SO2","NH3","FRP_MEAN"]

    for svar in vars_emis:
        print(svar)
        srcfield = ESMF.Field(srcgrid, name=svar)
        tgtfield = ESMF.Field(tgtgrid, name=svar)

        if svar=='FRP_MEAN':
            Store_by_Level(fout,'MeanFRP','Mean Fire Radiative Power','MW','3D','0.f','1.f')
        else:
            Store_by_Level(fout,svar,svar+' Biomass Emissions','kg m-2 s-1','3D','0.f','1.f')

        src_rate = ds_togid[svar].fillna(0)/area
        src_QA=xr.where(QA>1,src_rate,0.0,keep_attrs=True)

    for hr in range(0,24,1):
        print(hr)
        srcfield.data[...] = src_QA[hr,:,:]
        tgtfield = regridder(srcfield, tgtfield)

        if svar=='FRP_MEAN':
            tgt_rate = tgtfield.data*(tgt_area*1.e-6)
            fout.variables['MeanFRP'][hr,:,:] = tgt_rate
        else:
            tgt_rate = tgtfield.data*1.e-6/3600
            fout.variables[svar][hr,:,:] = tgt_rate 

    fout.close()


def Store_time_by_Level(fout,varname,var,long_name,year,mm,dd,cyc,DATE1):
    if varname=='time':
        var_out = fout.createVariable(varname, 'f4', ('Time',))
        var_out.long_name = long_name
        var_out.standard_name = long_name
        fout.variables[varname][:]=var
        var_out.units = 'hours since '+year+'-'+mm+'-'+dd+' '+cyc+':00:00'
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


# Main call ===================================================== CHJ =====
if __name__ == '__main__':
    intpl_ESMPy_QC_allspecies(sys.argv[1:])
