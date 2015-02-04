#-------------------------------------------------------------------------------
# Name:        test_nansatshape
# Purpose:      Test the Nansatshape class
#
# Author:       Asuka Yamakawa
#
# Created:     02.02.2015
# Copyright:   (c) NERSC
# Licence:      This file is part of NANSAT. You can redistribute it or modify
#               under the terms of GNU General Public License, v.3
#               http://www.gnu.org/licenses/gpl-3.0.html
#-------------------------------------------------------------------------------
import unittest
import warnings
import os
import sys

import numpy as np
from osgeo import osr

from nansat import Nansat, Domain
from nansat.nansatshape import Nansatshape


import nansat_test_data as ntd

class NansatmapTest(unittest.TestCase):
    def setUp(self):
        self.test_file_shape = os.path.join(ntd.test_data_path,
                                            'shape/points.shp')

        if not os.path.exists(self.test_file_shape):
            raise ValueError('No test data available')

    def test_init_from_nansatshape(self):
        nshape = Nansatshape(fileName=self.test_file_shape)

        self.assertTrue(isinstance(nshape, Nansatshape))

    def test_get_points(self):
        nshape = Nansatshape(fileName=self.test_file_shape)
        points, latlon = nshape.get_points()

        self.assertEqual(len(points), 10)
        self.assertTrue(latlon)

    def test_add_features(self):
        lonVector = [28.246011672, 28.2402443544, 28.2344793666]
        latVector = [71.5414916744, 71.5373746454, 71.5332574472]
        fieldValues = np.zeros(3, dtype={'names': ['X', 'Y'],
                                         'formats': ['i4', 'i4']})
        fieldValues['X'] = [14, 26, 20]
        fieldValues['Y'] = [50, 85, 39]

        nshape1 = Nansatshape(srs = osr.SpatialReference(osr.SRS_WKT_WGS84))
        nshape1.add_features(coordinates=np.array([lonVector, latVector]),
                        values=fieldValues)
        tmpfilename = os.path.join(ntd.tmp_data_path,
                                   'nansatshape_add_features.shp')
        nshape1.export(tmpfilename)

        nshape2 = Nansatshape(fileName=tmpfilename)
        points, latlon = nshape2.get_points()

        self.assertTrue(os.path.exists(tmpfilename))
        self.assertEqual(len(points), 3)
        self.assertTrue(latlon)


if __name__ == "__main__":
    unittest.main()



