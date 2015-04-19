# Name:         mapper_hirlam.py
# Purpose:      Nansat mapping for Hirlam model data
#               (GRIB files from www.yr.no)
# Authors:      Knut-Frode Dagestad, Morten W. Hansen
# Licence:      This file is part of NANSAT. You can redistribute it or modify
#               under the terms of GNU General Public License, v.3
#               http://www.gnu.org/licenses/gpl-3.0.html
import datetime

import numpy

from nansat.vrt import VRT
from nansat.tools import WrongMapperError


class Mapper(VRT):
    ''' VRT with mapping of WKV for HIRLAM '''

    def __init__(self, fileName, gdalDataset, gdalMetadata, **kwargs):

        try:
            geo_transform = gdalDataset.GetGeoTransform()[0:5]
        except AttributeError:
            raise WrongMapperError
        if geo_transform != (-12.1, 0.2, 0.0, 81.95, 0.0):
            raise WrongMapperError

        metaDict = [{'src': {'SourceFilename': fileName,
                             'SourceBand': 2,
                             'NODATA': 9999},
                     'dst': {'wkv': 'eastward_wind',
                             'height': '10 m'}
                     },
                    {'src': {'SourceFilename': fileName,
                             'SourceBand': 3,
                             'NODATA': 9999},
                     'dst': {'wkv': 'northward_wind',
                             'height': '10 m'}
                     },
                    {'src': [{'SourceFilename': fileName,
                              'SourceBand': 2,
                              'DataType': gdalDataset.GetRasterBand(2).DataType
                              },
                             {'SourceFilename': fileName,
                              'SourceBand': 3,
                              'DataType': gdalDataset.GetRasterBand(3).DataType
                              }],
                     'dst': {'wkv': 'wind_speed',
                             'name': 'windspeed',
                             'height': '10 m',
                             'PixelFunctionType': 'UVToMagnitude',
                             'NODATA': 9999}
                     },
                    {'src': [{'SourceFilename': fileName,
                              'SourceBand': 2,
                              'DataType': gdalDataset.GetRasterBand(2).DataType
                              },
                             {'SourceFilename': fileName,
                              'SourceBand': 3,
                              'DataType': gdalDataset.GetRasterBand(3).DataType
                              }],
                     'dst': {'wkv': 'wind_from_direction',
                             'name': 'winddirection',
                             'height': '10 m',
                             'PixelFunctionType': 'UVToDirectionFrom',
                             'NODATA': 9999
                             }
                     }]

        # create empty VRT dataset with geolocation only
        VRT.__init__(self, gdalDataset)

        # Create bands
        self._create_bands(metaDict)

        # Adding valid time from the GRIB file to dataset
        band = gdalDataset.GetRasterBand(2)
        validTime = band.GetMetadata()['GRIB_VALID_TIME']
        self._set_time(datetime.datetime.
                       utcfromtimestamp(int(validTime.strip().split(' ')[0])))

        return
