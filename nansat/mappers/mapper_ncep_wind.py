# Name:         mapper_ncep_wind
# Purpose:      Nansat mapping for NCEP GFS model data subset as downloaded
#               by mapper_ncep_wind_online
# Author:       Knut-Frode Dagestad
# Licence:      This file is part of NANSAT. You can redistribute it or modify
#               under the terms of GNU General Public License, v.3
#               http://www.gnu.org/licenses/gpl-3.0.html
#
# Made for GRIB files downloaded from http://nomads.ncep.noaa.gov/data/gfs4/
import datetime

from nansat.vrt import VRT
from nansat.tools import WrongMapperError


class Mapper(VRT):
    ''' VRT with mapping of WKV for NCEP GFS '''

    def __init__(self, fileName, gdalDataset, gdalMetadata, **kwargs):
        ''' Create NCEP VRT '''

        if not gdalDataset:
            raise WrongMapperError

        geotransform = gdalDataset.GetGeoTransform()
        if (geotransform != (-0.25, 0.5, 0.0, 90.25, 0.0, -0.5) or
                gdalDataset.RasterCount != 2):  # Not water proof
            raise WrongMapperError

        metaDict = [{'src': {'SourceFilename': fileName,
                             'SourceBand': 1},
                     'dst': {'wkv': 'eastward_wind',
                             'height': '10 m'}},
                    {'src': {'SourceFilename': fileName,
                             'SourceBand': 2},
                     'dst': {'wkv': 'northward_wind',
                             'height': '10 m'}},
                    {'src': [{'SourceFilename': fileName,
                              'SourceBand': 1,
                              'DataType': gdalDataset.GetRasterBand(1).DataType
                              },
                             {'SourceFilename': fileName,
                              'SourceBand': 2,
                              'DataType': gdalDataset.GetRasterBand(2).DataType
                              }],
                     'dst': {'wkv': 'wind_speed',
                             'PixelFunctionType': 'UVToMagnitude',
                             'name': 'windspeed',
                             'height': '2 m'
                             }},
                    {'src': [{'SourceFilename': fileName,
                              'SourceBand': 1,
                              'DataType': gdalDataset.GetRasterBand(1).DataType
                              },
                             {'SourceFilename': fileName,
                              'SourceBand': 2,
                              'DataType': gdalDataset.GetRasterBand(2).DataType
                              }],
                     'dst': {'wkv': 'wind_from_direction',
                             'PixelFunctionType': 'UVToDirectionFrom',
                             'name': 'winddirection',
                             'height': '2 m'
                             }
                     }]

        # create empty VRT dataset with geolocation only
        VRT.__init__(self, gdalDataset)

        # add bands with metadata and corresponding values to the empty VRT
        self._create_bands(metaDict)

        # Adding valid time from the GRIB file to dataset
        validTime = gdalDataset.GetRasterBand(1).\
            GetMetadata()['GRIB_VALID_TIME']
        self._set_time(datetime.datetime.
                       utcfromtimestamp(int(validTime.strip().split(' ')[0])))

        return
