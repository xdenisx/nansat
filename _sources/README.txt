.. image:: http://nansencenter.github.io/nansat/images/nansat_logo.png

Nansat is a scientist friendly Python toolbox for processing 2D geospatial data.

The main purpose of Nansat is to facilitate:

* easy development and testing of scientific algorithms,
* easy analysis of geospatial data, and
* efficient operational processing.

:note:
    We appreciate acknowledments of Nansat. Please add "The image analysis was performed with
    the open-source NanSat (https://github.com/nansencenter/nansat) python package" (or equivalent)
    if you use Nansat in scientific publications.

=========
Install
=========
First install required libraries. The easies way is to use a Python distribution. E.g. `Anaconda <https://store.continuum.io/cshop/anaconda/>`_

::

    # download the minimal anaconda distribution
    wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh

    # make the installer executable
    chmod +x miniconda.sh

    # run the installer and let it install miniconda
    # into your home directory
    ./miniconda.sh -b -p $HOME/miniconda

    # set the path to contain miniconda executables first
    # add this line in the end of your .bashrc
    # to make the miniconda work next time
    export PATH=$HOME/miniconda/bin:$PATH

    # update the anaconda distro
    # 'conda' is the command to manipulate with the distro
    conda update --yes conda

    # install the required packages into
    # $HOME/miniconda/lib/python2.7/site-packages
    # in addition that will install all the requirements
    conda install --yes ipython setuptools numpy scipy gdal pillow basemap nose

    # install GDAL data files from jjhelmus repo
    # which is not included by default in anaconda.gdal
    # https://groups.google.com/a/continuum.io/forum/#!topic/anaconda/608MwtlekKk
    conda install -c jjhelmus gdal-data

    # add path to the gdal data (add that to your .bashrc)
    export GDAL_DATA=$HOME/miniconda/share/gdal

    # install proj4 library from rsignell repo
    # not included in the anaconda repo by default
    conda install -c rsignell proj4

Read more about installtion `here <https://github.com/nansencenter/nansat/wiki/Required-libs
>_`

Now get copy of Nansat and run installation
::

    git clone https://github.com/nansencenter/nansat.git
    cd nansat
    python setup.py install

Test if everything was installed correctly
::

    cd ~/
    nosetests nansat.tests

=====
Usage
=====
::

    # open your favorite satellite image
    n = Nansat('satellite_image_filename.tif')

    # inspect  the conent of the file
    print n

    # fetch numpy array with data from the first band
    arr1 = n[1]

    # if you know the name of the band,
    # access data by name, e.g.
    arr2 = n['SST']

    # write a simple image in graphical format
    n.write_figure('figure_fileame.png', ['SST'], clim=[-2, 15])

    # define a new lat/lon grid, using EPSG code
    # and parameters for ``gdaltransform``
    d = Domain(4326, '-te -5 50 10 70 -ts 150 200')

    # reproject your image onto the defined grid
    # and fetch reprojected data
    n.reproject(d)
    arr3 = n[1]

For more details see `Tutorial <https://github.com/nansencenter/nansat/wiki/Tutorial>`_

