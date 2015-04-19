# Name:        nansat_mapper_merisL1
# Purpose:     Mapping for Meris-L1 data
# Authors:      Anton Korosov
# Licence:      This file is part of NANSAT. You can redistribute it or modify
#               under the terms of GNU General Public License, v.3
#               http://www.gnu.org/licenses/gpl-3.0.html
from pytz import UTC
from dateutil.parser import parse

from nansat.vrt import VRT
from nansat.tools import WrongMapperError
from envisat import Envisat


class Mapper(VRT, Envisat):
    ''' VRT with mapping of WKV for MERIS Level 1 (FR or RR) '''

    def __init__(self, fileName, gdalDataset, gdalMetadata,
                 geolocation=False, zoomSize=500, step=1, **kwargs):

        ''' Create MER1 VRT

        Parameters
        -----------
        fileName : string

        gdalDataset : gdal dataset

        gdalMetadata : gdal metadata

        geolocation : bool (default is False)
            if True, add gdal geolocation

        zoomSize: int (used in envisat.py)
            size, to which the ADS array will be zoomed using scipy
            array of this size will be stored in memory

        step: int (used in envisat.py)
            step of pixel and line in GeolocationArrays. lat/lon grids are
            generated at that step

        '''

        self.setup_ads_parameters(fileName, gdalMetadata)

        if (self.product[0:9] != "MER_FRS_1" and
                self.product[0:9] != "MER_RR__1"):
            raise WrongMapperError

        metaDict = [{'src': {'SourceFilename': fileName, 'SourceBand': 1},
                     'dst': {'wkv': 'toa_outgoing_spectral_radiance',
                             'wavelength': '413'}},
                    {'src': {'SourceFilename': fileName, 'SourceBand': 2},
                     'dst': {'wkv': 'toa_outgoing_spectral_radiance',
                             'wavelength': '443'}},
                    {'src': {'SourceFilename': fileName, 'SourceBand': 3},
                     'dst': {'wkv': 'toa_outgoing_spectral_radiance',
                             'wavelength': '490'}},
                    {'src': {'SourceFilename': fileName, 'SourceBand': 4},
                     'dst': {'wkv': 'toa_outgoing_spectral_radiance',
                             'wavelength': '510'}},
                    {'src': {'SourceFilename': fileName, 'SourceBand': 5},
                     'dst': {'wkv': 'toa_outgoing_spectral_radiance',
                             'wavelength': '560'}},
                    {'src': {'SourceFilename': fileName, 'SourceBand': 6},
                     'dst': {'wkv': 'toa_outgoing_spectral_radiance',
                             'wavelength': '620'}},
                    {'src': {'SourceFilename': fileName, 'SourceBand': 7},
                     'dst': {'wkv': 'toa_outgoing_spectral_radiance',
                             'wavelength': '665'}},
                    {'src': {'SourceFilename': fileName, 'SourceBand': 8},
                     'dst': {'wkv': 'toa_outgoing_spectral_radiance',
                             'wavelength': '681'}},
                    {'src': {'SourceFilename': fileName, 'SourceBand': 9},
                     'dst': {'wkv': 'toa_outgoing_spectral_radiance',
                             'wavelength': '709'}},
                    {'src': {'SourceFilename': fileName, 'SourceBand': 10},
                     'dst': {'wkv': 'toa_outgoing_spectral_radiance',
                             'wavelength': '753'}},
                    {'src': {'SourceFilename': fileName, 'SourceBand': 11},
                     'dst': {'wkv': 'toa_outgoing_spectral_radiance',
                             'wavelength': '761'}},
                    {'src': {'SourceFilename': fileName, 'SourceBand': 12},
                     'dst': {'wkv': 'toa_outgoing_spectral_radiance',
                             'wavelength': '778'}},
                    {'src': {'SourceFilename': fileName, 'SourceBand': 13},
                     'dst': {'wkv': 'toa_outgoing_spectral_radiance',
                             'wavelength': '864'}},
                    {'src': {'SourceFilename': fileName, 'SourceBand': 14},
                     'dst': {'wkv': 'toa_outgoing_spectral_radiance',
                             'wavelength': '849'}},
                    {'src': {'SourceFilename': fileName, 'SourceBand': 15},
                     'dst': {'wkv': 'toa_outgoing_spectral_radiance',
                             'wavelength': '900'}},
                    {'src': {'SourceFilename': fileName, 'SourceBand': 16,
                             'DataType': 1},
                     'dst': {'wkv': 'quality_flags', 'suffix': 'l1'}}
                    ]

        # add DataType into 'src' and suffix into 'dst'
        for bandDict in metaDict:
            if 'DataType' not in bandDict['src']:
                # default for meris L1 DataType UInt16
                bandDict['src']['DataType'] = 2
            if 'wavelength' in bandDict['dst']:
                bandDict['dst']['suffix'] = bandDict['dst']['wavelength']

        # get scaling GADS from header
        scales = self.read_scaling_gads(range(7, 22))
        # set scale factor to the band metadata (only radiances)
        for i, bandDict in enumerate(metaDict[:-1]):
            bandDict['src']['ScaleRatio'] = str(scales[i])

        # get list with resized VRTs from ADS
        self.bandVRTs = {'adsVRTs': self.get_ads_vrts(gdalDataset,
                                                     ['sun zenith angles',
                                                      'sun azimuth angles',
                                                      'zonal winds',
                                                      'meridional winds'],
                                                     zoomSize=zoomSize,
                                                     step=step)}
        # add bands from the ADS VRTs
        for adsVRT in self.bandVRTs['adsVRTs']:
            metaDict.append({'src': {'SourceFilename': adsVRT.fileName,
                                     'SourceBand': 1},
                             'dst': {'name': (adsVRT.dataset.GetRasterBand(1).
                                              GetMetadataItem('name')),
                                     'units': (adsVRT.dataset.GetRasterBand(1).
                                               GetMetadataItem('units'))}
                             })

        # create empty VRT dataset with geolocation only
        VRT.__init__(self, gdalDataset)

        # add bands with metadata and corresponding values to the empty VRT
        self._create_bands(metaDict)

        # set time
        self._set_envisat_time(gdalMetadata)

        # set SADCAT specific metadata
        self.dataset.SetMetadataItem('start_date',
                                     (parse(
                                      gdalMetadata['SPH_FIRST_LINE_TIME']).
                                      isoformat()
                                      + '+00:00'))
        self.dataset.SetMetadataItem('stop_date',
                                     (parse(
                                      gdalMetadata['SPH_LAST_LINE_TIME']).
                                      isoformat()
                                      + '+00:00'))
        self.dataset.SetMetadataItem('sensor', 'MERIS')
        self.dataset.SetMetadataItem('satellite', 'ENVISAT')
        self.dataset.SetMetadataItem('mapper', 'meris_l1')

        # add geolocation arrays
        if geolocation:
            self.add_geolocation_from_ads(gdalDataset,
                                          zoomSize=zoomSize, step=step)
