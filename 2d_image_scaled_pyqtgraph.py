
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
    def __init__(self):
        PyQt4.QtGui.QWidget.__init__(self)

        self.plotItem  = pg.PlotItem()
        self.imageView = pg.ImageView(view = self.plotItem)
        self.imageItem = self.imageView.getImageItem()

        self.imageView.ui.menuBtn.hide()
        self.imageView.ui.roiBtn.hide()

    def show(self, array):
        self.imageView.setImage(array)
        self.imageView.show()


signal.signal(signal.SIGINT, signal.SIG_DFL)
app = PyQt4.QtGui.QApplication(sys.argv)

im = Show_2darray_with_axes()

im.show(np.random.random((20,10)))

sys.exit(app.exec_())
