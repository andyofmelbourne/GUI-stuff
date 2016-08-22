
# python 2/3 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# make an image widget that has an aspect ratio 
# and labeled axes

import pyqtgraph as pg
import PyQt4.uic
import PyQt4.QtGui
import sys, os, signal

import numpy as np

class Show_2darray_with_axes(PyQt4.QtGui.QWidget):
    def __init__(self, title = None, labels={'bottom': ('x axis title', 'm'), 'left': ('y axis title', 'm')}, \
                 ss_min_max=None, fs_min_max=None, aspect='equal'):
        PyQt4.QtGui.QWidget.__init__(self)

        # delay initialisation until we see the first image
        # this is because we have to pass the plot widget
        # to ImageView
        self.imageView = None

        self.plt = pg.PlotItem(title = title, labels = labels)

        self.ss_min_max = ss_min_max
        self.fs_min_max = fs_min_max
        self.aspect = aspect

    def show(self, array, init = False):
        if self.imageView is None :
            init = True
            self.imageView = pg.ImageView(view = self.plt)
            self.imageView.ui.menuBtn.hide()
            self.imageView.ui.roiBtn.hide()
            self.imageView.show()

        if (self.ss_min_max is not None) and (self.fs_min_max is not None) :
            pos    = [self.fs_min_max[0], self.ss_min_max[0]]
            yscale = (self.ss_min_max[1] - self.ss_min_max[0]) / array.shape[0]
            xscale = (self.fs_min_max[1] - self.fs_min_max[0]) / array.shape[1]
            scale  = [xscale, yscale]
        else :
            scale = pos = None
        
        if init :
            self.imageView.setImage(array.T, pos=pos, scale=scale)
        else :
            self.imageView.setImage(array.T, pos=pos, scale=scale, 
                    autoRange = False, autoLevels = False, autoHistogramRange = False)
        
        if self.aspect == 'equal' :
            self.plt.setAspectLocked(False)

if __name__ == '__main__':

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = PyQt4.QtGui.QApplication(sys.argv)

    # let's say we have a 2d array of random numbers shape = (20, 10)
    # and they represent data with: slow-scan values -2 to 10 seconds
    #                               fast-scan values 5.0e-3 to 20.0e-3 meters
    labels = {'bottom' : ('distance', 'm'), 'left' : ('time', 's')}
    title  = 'example plot'

    #array = np.random.random((20,10))
    fs = np.linspace(5.0e-3, 20.0e-3, 10)
    ss = np.linspace(-2, 10, 20)
    ss_min_max = [ss.min(), ss.max()]
    fs_min_max = [fs.min(), fs.max()]

    ss, fs = np.meshgrid(ss, fs, indexing='ij')

    # this is now the image Widget
    im = Show_2darray_with_axes(title, labels, ss_min_max, fs_min_max)

    array = np.sqrt( ss**2 + (1.0e3*fs)**2)

    # run the widget within our 'app' application
    im.show(array)

    sys.exit(app.exec_())
