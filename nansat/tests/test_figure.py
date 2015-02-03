#-------------------------------------------------------------------------------
# Name:        test_figure
# Purpose:      Test the Figure class
#
# Author:       Asuka Yamakawa
#
# Created:     02.02.2015
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

from nansat import Nansat, Domain, Figure

import nansat_test_data as ntd

class NansatmapTest(unittest.TestCase):
    def setUp(self):
        self.test_file_gcps = os.path.join(ntd.test_data_path, 'gcps.tif')
        self.test_file_map= os.path.join(ntd.test_data_path, 'map.tif')
        self.nansat_logo= os.path.join(ntd.test_data_path, 'nansat_logo_s.png')
        plt.switch_backend('Agg')

        if not os.path.exists(self.test_file_map):
            raise ValueError('No test data available')

    def test_init_from_figure(self):
        n = Nansat(self.test_file_gcps, logLevel=40)
        fig = Figure(n[1])

        self.assertTrue(isinstance(fig, Figure))

    def test_add_grids_labels(self):
        n = Nansat(self.test_file_gcps, logLevel=40)
        lons, lats = n.get_geolocation_grids()
        fig = Figure(n[1])
        tmpfilename = os.path.join(ntd.tmp_data_path,
                                   'figure_add_grids_labels.png')
        fig._create_palette()
        fig.add_latlon_grids(latGrid=lats, lonGrid=lons)
        fig.create_pilImage()
        fig.add_latlon_labels(latlonLabels=True, fontSize=8,
                              latTicks=5, lonTicks=5)
        fig.save(tmpfilename)

        self.assertTrue(os.path.exists(tmpfilename))

    def test_clip(self):
        n = Nansat(self.test_file_gcps, logLevel=40)
        fig = Figure(n[1])
        tmpfilename = os.path.join(ntd.tmp_data_path,
                                   'figure_create_clip.png')
        fig.clip(cmin=15, cmax=40)
        fig.convert_palettesize()
        fig._create_palette()
        fig.create_pilImage()
        fig.save(tmpfilename)

        self.assertEqual(fig.cmin[0], 15.0)
        self.assertEqual(fig.cmax[0], 40.0)
        self.assertTrue(os.path.exists(tmpfilename))

    def test_create_legend(self):
        n = Nansat(self.test_file_gcps, logLevel=40)
        fig = Figure(n[1])
        tmpfilename = os.path.join(ntd.tmp_data_path,
                                   'figure_create_legend.png')
        fig.convert_palettesize()
        fig._create_palette()
        fig.create_legend(fontSize=5)
        fig.create_pilImage()
        fig.save(tmpfilename)

        self.assertTrue(os.path.exists(tmpfilename))

    def test_histogram(self):
        n = Nansat(self.test_file_gcps, logLevel=40)
        fig = Figure(n[1])
        tmpfilename = os.path.join(ntd.tmp_data_path,
                                   'figure_histogram.png')
        clim = fig.clim_from_histogram(ratio=0.8)
        fig.clip(cmin=clim[0], cmax=clim[1])
        fig.convert_palettesize()
        fig._create_palette()
        fig.create_pilImage()
        fig.save(tmpfilename)

        self.assertTrue(fig.cmin[0] > 8.0)
        self.assertTrue(fig.cmax[0] < 52.0)
        self.assertTrue(os.path.exists(tmpfilename))

    def test_logarithm(self):
        n = Nansat(self.test_file_gcps, logLevel=40)
        fig = Figure(n[1])
        tmpfilename = os.path.join(ntd.tmp_data_path, 'figure_logarithm.png')
        fig.apply_logarithm(gamma=0.8)
        fig._create_palette()
        fig.create_pilImage()
        fig.save(tmpfilename)

        self.assertTrue(os.path.exists(tmpfilename))

    def test_logo(self):
        n = Nansat(self.test_file_gcps, logLevel=40)
        fig = Figure(n[1])
        tmpfilename = os.path.join(ntd.tmp_data_path, 'figure_logo.png')
        fig._create_palette()
        fig.create_pilImage()
        fig.add_logo(logoFileName=self.nansat_logo, logoSize=[60, 45])
        fig.save(tmpfilename)

        self.assertTrue(os.path.exists(tmpfilename))

    def test_mask(self):
        n = Nansat(self.test_file_gcps, logLevel=40)
        fig = Figure(n[1])
        tmpfilename = os.path.join(ntd.tmp_data_path, 'figure_mask.png')
        wmArray = n.watermask()[1]
        fig = Figure(n[1])
        fig._create_palette()
        fig.apply_mask(mask_array=wmArray, mask_lut={1: [150, 150, 150]})
        fig.create_pilImage()
        fig.save(tmpfilename)

        self.assertTrue(os.path.exists(tmpfilename))

    def test_palettesize(self):
        n = Nansat(self.test_file_gcps, logLevel=40)
        fig = Figure(n[1])
        tmpfilename = os.path.join(ntd.tmp_data_path, 'figure_palettesize.png')
        fig.convert_palettesize()
        fig._create_palette()
        fig.create_pilImage()
        fig.save(tmpfilename)

        self.assertTrue(os.path.exists(tmpfilename))

    def test_process(self):
        n = Nansat(self.test_file_gcps, logLevel=40)
        fig = Figure(n[1])
        tmpfilename = os.path.join(ntd.tmp_data_path, 'figure_process.png')
        fig.process(cmin=10, cmax=45)
        fig.save(tmpfilename)

        self.assertTrue(os.path.exists(tmpfilename))

    def test_process_rgb(self):
        n = Nansat(self.test_file_gcps, logLevel=40)
        w, h = n[1].shape
        tmpfilename = os.path.join(ntd.tmp_data_path, 'figure_rgb.png')
        array1 = n[1].reshape(1, w, h)
        array2 = n[2].reshape(1, w, h)
        array3 = n[3].reshape(1, w, h)
        array1 = np.append(array1, array2, axis=0)
        array1 = np.append(array1, array3, axis=0)
        fig = Figure(array1)
        fig.process(cmin=[20, 10, 10], cmax=[50, 30, 30])
        fig.save(tmpfilename)

        self.assertTrue(os.path.exists(tmpfilename))

    def test_save(self):
        n = Nansat(self.test_file_gcps, logLevel=40)
        fig = Figure(n[1])
        tmpfilename = os.path.join(ntd.tmp_data_path, 'figure_save.png')
        fig._create_palette()
        fig.create_pilImage()
        fig.save(tmpfilename)

        self.assertTrue(os.path.exists(tmpfilename))


if __name__ == "__main__":
    unittest.main()






