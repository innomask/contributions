'''
 File Name: oneAU_enso.py
 Description: Code to make the graphs seen in the "ENSO Events and the Amazon Basin: Basic Aspects" text.
 Author: Willy Hagi
 E-mail: hagi.willy@gmail.com
 Python Version: 3.6
'''


import matplotlib.pyplot as plt
import cartopy.feature as cf
import cartopy.crs as ccrs
import seaborn as sns
import proplot as plot # (not so) secret ingredient
import xarray as xr
import numpy as np

from cartopy.feature import ShapelyFeature
from cartopy.io.shapereader import Reader


# Fig. 1
'''
The dataset to plot the ENSO patterns is a detrended sea surface temperature anomaly (SSTA)
with respect to the 1981-2010 climatological mean and it was created from the original
Extended Reconstructed Sea Surface Temperature (ERSSTv5) from PSD/NOAA.
Link: https://www.esrl.noaa.gov/psd/data/gridded/data.noaa.ersst.v5.html
'''

dset = xr.open_dataset('asstdt_wrt8110.nc')
sst = dset['sst']

# select the 2010/2011 La Niña and 2015/2016 El Niño
nino_2015 = sst.sel(time=slice('2015-12-01', '2016-02-01')).groupby('time.season').mean('time')
nina_2010 = sst.sel(time=slice('2010-12-01', '2011-02-01')).groupby('time.season').mean('time')

# proplot
f, ax = plot.subplots(axwidth=6., nrows=2, tight=True, proj='pcarree',
                      proj_kw={'lon_0': 180}, panel='b')

# a wrap-around to plot longitude ticks correctly
longitude = np.append(np.arange(-160, -40, 20), np.arange(100, 200, 20), axis=0)

# plot formatting options
ax.format(land=True, coast=True, innerborders=True, borders=True, landcolor='grey',
          large='15px',
          geogridlinewidth=0, labels=True,
          latlim=(-31, 31), lonlim=(100, 300),
          lonlines = longitude, latlines = np.arange(-30, 40, 10))

map1 = ax[0].contourf(sst['lon'], sst['lat'], nino_2015[0,:,:],
                      levels=np.arange(-2.0, 2.5, 0.5), cmap='NegPos', extend='both')
ax[0].format(title='a) El Niño - 2015/2016')

map2 = ax[1].contourf(sst['lon'], sst['lat'], nina_2010[0,:,:],
                      levels=np.arange(-2.0, 2.5, 0.5), cmap='NegPos', extend='both')
ax[1].format(title='b) La Niña - 2010/2011')

f.bpanel.colorbar(map1, label='SSTA', length=0.5, extendrect=True)

f.save('ssta_enso.jpeg', dpi=300)

plt.show()



# Fig. 2
'''
This dataset is for rainfall satellite estimations from the PERSIANN platform
only for the Amazon Basin area.

You can easily select the area and download the data at the Portal: https://chrsdata.eng.uci.edu/
The shapefile for the Basin comes with the data.
'''

dset = xr.open_dataset('CDR_amazonbasin.nc')
# masking undefined values outside the basin area
dset['precip'] = dset['precip'].where(dset['precip'] != -99.)
# seasonal cycle
season = dset['precip'].groupby('datetime.season').mean('datetime')

basin = 'amazon_shape.shp' # shapefile
proj  =  ccrs.PlateCarree() # cartopy projection

f, ax = plot.subplots(axwidth=3.5, nrows=2, ncols=2, tight=True, proj='pcarree',
                      proj_kw={'lon_0':180},)

ax.format(land=False, coast=True, innerborders=True, borders=True, grid=False,
          geogridlinewidth=0, labels=True,
          latlim=(-21, 12), lonlim=(275, 315),
          latlines=plot.arange(-20, 10, 5), lonlines=plot.arange(-95, -20, 5),
          large='15px')

map1 = ax[0,0].contourf(dset['lon'], dset['lat'], season[0,:,:],
                     cmap='BuPu', levels=np.arange(50, 500, 50), extend='both')
map2 = ax[0,1].contourf(dset['lon'], dset['lat'], season[2,:,:],
                     cmap='BuPu', levels=np.arange(50, 500, 50), extend='both')
map3 = ax[1,0].contourf(dset['lon'], dset['lat'], season[1,:,:],
                     cmap='BuPu', levels=np.arange(50, 500, 50), extend='both')
map4 = ax[1,1].contourf(dset['lon'], dset['lat'], season[3,:,:],
                     cmap='BuPu', levels=np.arange(50, 500, 50), extend='both')

ax[1,0].colorbar(map3, loc='b', label='mm/month', shrink=0.1)
ax[1,1].colorbar(map4, loc='b', label='mm/month', shrink=0.1)

ax[0,0].format(title='DJF')
ax[0,1].format(title='MAM')
ax[1,0].format(title='JJA')
ax[1,1].format(title='SON')

ax[0,0].add_geometries(Reader(basin).geometries(), proj, edgecolor='black', facecolor='none')
ax[0,1].add_geometries(Reader(basin).geometries(), proj, edgecolor='black', facecolor='none')
ax[1,0].add_geometries(Reader(basin).geometries(), proj, edgecolor='black', facecolor='none')
ax[1,1].add_geometries(Reader(basin).geometries(), proj, edgecolor='black', facecolor='none')

f.save('rainfall_seasonality.jpeg')

plt.show()


# Fig. 3
'''
This is the Standardized Precipitation-Evaporation Index (SPEI) from the Global SPEI database.
Link: https://spei.csic.es/home.html

'''
dset = xr.open_dataset('spei01.nc')
spei = dset['spei']


nino_2015 = spei.sel(time=slice('2015-12-01', '2016-02-01')).groupby('time.season').mean('time')
nina_2010 = spei.sel(time=slice('2010-12-01', '2011-02-01')).groupby('time.season').mean('time')


f, ax = plot.subplots(axwidth=4., nrows=1, ncols=2, tight=True, proj='pcarree',
                      proj_kw={'lon_0': 0}, panel='b')

ax.format(land=False, coast=True, innerborders=True, borders=True,
          large='25px', small='20px',
          geogridlinewidth=0, labels=True,
          latlim=(-21, 12), lonlim=(275, 315),
          lonlines=np.arange(-180, 0, 10), latlines = np.arange(-20, 15, 5),)

map1 = ax[0].contourf(spei['lon'], spei['lat'], nino_2015[0,:,:],
                      levels=np.arange(-3.0, 3.5, 0.5), cmap='DryWet', extend='both')
ax[0].format(title='a) El Niño - 2015/2016')

map2 = ax[1].contourf(spei['lon'], spei['lat'], nina_2010[0,:,:],
                      levels=np.arange(-3.0, 3.5, 0.5), cmap='DryWet', extend='both')
ax[1].format(title='b) La Niña - 2010/2011')

f.bpanel.colorbar(map1, label='SPEI', length=0.5, extendrect=True)

ax[0].add_geometries(Reader(basin).geometries(), proj, edgecolor='black', facecolor='none')
ax[1].add_geometries(Reader(basin).geometries(), proj, edgecolor='black', facecolor='none')

f.save('spei_enso.jpeg', dpi=300)

plt.show()
