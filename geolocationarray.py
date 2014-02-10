# Name:    nansat.py
# Purpose: Container of VRT and GeolocationDomain classes
# Authors:      Asuka Yamakawa, Anton Korosov, Knut-Frode Dagestad,
#               Morten W. Hansen, Alexander Myasoyedov,
#               Dmitry Petrenko, Evgeny Morozov
# Created:      29.06.2011
# Copyright:    (c) NERSC 2011 - 2013
# Licence:
# This file is part of NANSAT.
# NANSAT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
# http://www.gnu.org/licenses/gpl-3.0.html
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
import tempfile

from nansat_tools import *


class GeolocationArray():
    '''Container for GEOLOCATION ARRAY data

    | Keeps references to bands with X and Y coordinates, offset and step
      of pixel and line. All information is stored in dictionary self.d
    |
    | Instance of GeolocationArray is used in VRT and ususaly created in
      a Mapper.
    '''
    def __init__(self, xVRT=None, yVRT=None,
                 xBand=1, yBand=1, srs='', lineOffset=0, lineStep=1,
                 pixelOffset=0, pixelStep=1, dataset=None):
        '''Create GeolocationArray object from input parameters

        Parameters
        -----------
        xVRT : VRT-object or str
            VRT with array of x-coordinates OR string with dataset source
        yVRT : VRT-object or str
            VRT with array of y-coordinates OR string with dataset source
        xBand : number of band in the xDataset
        xBand : number of band in the yDataset
        srs : str, WKT
        lineOffset : int, offset of first line
        lineStep : int, step of lines
        pixelOffset : int, offset of first pixel
        pixelStep : step of pixels
        dataset : GDAL dataset to take geolocation arrays from

        Attributes
        -----------
        X_DATASET
        Y_DATASET
        X_BAND
        Y_BAND
        SRS
        LINE_OFFSET
        LINE_STEP
        PIXEL_OFFSET
        PIXEL_STEP

        '''
        # dictionary with all metadata
        self.d = {}
        # VRT objects
        self.xVRT = None
        self.yVRT = None

        # make object from GDAL dataset
        if dataset is not None:
            self.d = dataset.GetMetadata('GEOLOCATION')
            return

        # make empty object
        if xVRT is None or yVRT is None:
            return

        if isinstance(xVRT, str):
            # make object from strings
            self.d['X_DATASET'] = xVRT
            self.d['Y_DATASET'] = yVRT
        else:
            # make object from VRTs
            self.xVRT = xVRT
            self.d['X_DATASET'] = xVRT.fileName
            self.yVRT = yVRT
            self.d['Y_DATASET'] = yVRT.fileName

        # proj4 to WKT
        if srs == '':
            sr = osr.SpatialReference()
            sr.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
            srs = sr.ExportToWkt()
        self.d['SRS'] = srs
        self.d['X_BAND'] = str(xBand)
        self.d['Y_BAND'] = str(yBand)
        self.d['LINE_OFFSET'] = str(lineOffset)
        self.d['LINE_STEP'] = str(lineStep)
        self.d['PIXEL_OFFSET'] = str(pixelOffset)
        self.d['PIXEL_STEP'] = str(pixelStep)

    def get_geolocation_grids(self):
        '''Read values of geolocation grids'''
        lonDS = gdal.Open(self.d['X_DATASET'])
        lonBand = lonDS.GetRasterBand(int(self.d['X_BAND']))
        lonGrid = lonBand.ReadAsArray()
        latDS = gdal.Open(self.d['Y_DATASET'])
        latBand = latDS.GetRasterBand(int(self.d['Y_BAND']))
        latGrid = latBand.ReadAsArray()

        return lonGrid, latGrid
