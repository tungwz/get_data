# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 19:56:24 2021

@author: ZongrAx
"""

import os
import cdsapi
import datetime
from multiprocessing import Process


def download(filepath, filename, var, pres, days, area):
    os.chdir(filepath)
    c = cdsapi.Client()
    # Copy the CDS API key, in the file $HOME/.cdsapirc (Linux/Unix) or
    # c = cdsapi.Client(url="xxx",
    #                  key="xxx")
    # set with your URL and API key
    # The following is set according to the ERA5 API
    # An example for ERA5 monthly averaged data on pressure levels from 1979 to present
    c.retrieve(
        'reanalysis-era5-pressure-levels-monthly-means',
        {
            'product_type': 'monthly_averaged_reanalysis',
            'format': 'netcdf',  # grib or netcdf
            'variable': var,
            'pressure_level': pres,
            'year': days[0:4],
            'month': days[-4:-2],
            # 'day'          : days[-2:],
            'time': '00:00',
            'area': area,  # nlat, wlon, slat, elon
        },
        filename)

    return 0


def main():
    syr = datetime.date(2020, 5, 1)  # star year
    eyr = datetime.date(2020, 7, 31)  # end year
    b = syr
    d = datetime.timedelta(days=1)

    var = ['divergence']  # add the vars you need
    pres = ['1000']  # add the pres levels you need
    area = [54, 73, 3, 136]
    filepath = r'E:/迅雷下载/'

    while b <= eyr:
        days = b.strftime("%Y%m%d")
        filename = 'era5_plevels'+days+'.nc'  # format: grib or nc

        plist = []

        p = Process(target=download, args=(filepath,
                                           filename, var, pres, days, area))
        p.start()
        plist.append(p)

        for p in plist:
            p.join()
            print("complete")

        b += d

    del p


if __name__ == '__main__':
    main()
