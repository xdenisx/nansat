#-------------------------------------------------------------------------------
# Name:        test_nansatmap
# Purpose:      Test the Nansatmap class
#
# Author:       Asuka Yamakawa
#
# Created:     29.01.2015
# Copyright:   (c) NERSC
# Licence:      This file is part of NANSAT. You can redistribute it or modify
#               under the terms of GNU General Public License, v.3
#               http://www.gnu.org/licenses/gpl-3.0.html
#------------------------------------------------------------------------------
import unittest
import warnings
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

from nansat import Nansat, Domain, Nansatmap

import nansat_test_data as ntd

class NansatmapTest(unittest.TestCase):
    def setUp(self):
        self.test_file_map= os.path.join(ntd.test_data_path, 'map.tif')
        plt.switch_backend('Agg')

        if not os.path.exists(self.test_file_map):
            raise ValueError('No test data available')

    def test_init_from_domain(self):
        d = Domain("+proj=latlong +datum=WGS84 +ellps=WGS84 +no_defs",
                   "-te 25 70 35 72 -ts 2000 2000")
        nMap = Nansatmap(d)

        self.assertEqual(type(nMap), Nansatmap)

    def test_init_from_nansat(self):
        n = Nansat(self.test_file_map, logLevel=40)
        nMap = Nansatmap(n, resolution='l')

        self.assertEqual(type(nMap), Nansatmap)

    def test_pcolormesh(self):
        n = Nansat(self.test_file_map, logLevel=40)
        nMap = Nansatmap(n)
        status = nMap.pcolormesh(n['windspeed'])

        self.assertEqual(status, 0)

    def test_pcolormesh_grid_colorbar(self):
        n = Nansat(self.test_file_map, logLevel=40)
        nMap = Nansatmap(n)
        status1 = nMap.pcolormesh(n['windspeed'], vmin=5.0, vmax=20.0)
        status2 = nMap.drawgrid()
        status3 = nMap.add_colorbar()

        self.assertEqual(status1 + status2 + status3, 0)

    def test_quiver(self):
        n = Nansat(self.test_file_map, logLevel=40)
        nMap = Nansatmap(n, resolution='l')
        status = nMap.quiver(dataX=n['east_wind'], dataY=n['north_wind'])

        self.assertEqual(status, 0)

    def test_quiver_set_step(self):
        n = Nansat(self.test_file_map, logLevel=40)
        nMap = Nansatmap(n)
        status = nMap.quiver(dataX=n['east_wind'], dataY=n['north_wind'],
                             step=20)

        self.assertEqual(status, 0)

    def test_contourf(self):
        n = Nansat(self.test_file_map, logLevel=40)
        nMap = Nansatmap(n)
        status = nMap.contourf(n['windspeed'], smooth=True)

        self.assertEqual(status, 0)

    def test_contourf_colorbar(self):
        n = Nansat(self.test_file_map, logLevel=40)
        nMap = Nansatmap(n)
        status1 = nMap.contourf(n['windspeed'])
        status2 = nMap.add_colorbar()

        self.assertEqual(status1 + status2, 0)

    def test_contour(self):
        n = Nansat(self.test_file_map, logLevel=40)
        nMap = Nansatmap(n)
        status = nMap.contour(n['windspeed'])

        self.assertEqual(status, 0)

    def test_contour_nomask(self):
        n = Nansat(self.test_file_map, logLevel=40)
        nMap = Nansatmap(n)
        status1 = nMap.contour(n['windspeed'], v=[20, 16, 12, 8, 4])
        tmpfilename = os.path.join(ntd.tmp_data_path,
                                   'nansatshape_contour.png')
        status2 = nMap.save(tmpfilename, landmask=True)

        self.assertEqual(status1 + status2, 0)
        self.assertTrue(os.path.exists(tmpfilename))

    def test_imshow(self):
        n = Nansat(self.test_file_map, logLevel=40)
        nMap = Nansatmap(n)
        w, h= n[1].shape
        array1 = n[1].reshape(w, h, 1)
        array2 = n[2].reshape(w, h, 1)
        array3 = n[3].reshape(w, h, 1)
        array1 = np.append(array1, array2, axis=2)
        array1 = np.append(array1, array3, axis=2)
        status = nMap.imshow(array1)

        self.assertEqual(status, 0)


if __name__ == "__main__":
    unittest.main()
