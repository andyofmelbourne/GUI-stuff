from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys, os
import numpy as np
import h5py
import scipy.constants as sc
import signal
import copy 

try :
    from ConfigParser import ConfigParser 
except ImportError :
    from configparser import ConfigParser 

try :
    from PyQt5 import QtCore, QtGui
except :
    from PyQt4 import QtCore, QtGui

from collections import OrderedDict

class Write_config_file_widget(QtGui.QWidget):
    def __init__(self, config_fnam, output_filename = None):
        super(Write_config_file_widget, self).__init__()
        
        # read the input config file
        config = ConfigParser()
        config.read(config_fnam)
        self.params_input = copy.deepcopy(config._sections)
        self.params       = copy.deepcopy(self.params_input)
        
        # set the output filename 
        if output_filename is None :
            self.output_filename = config_fnam
        else :
            self.output_filename = output_filename
        self.initUI(self.params)
    
    def initUI(self, params):
        # Make a grid layout
        layout = QtGui.QGridLayout()
        
        # add the layout to the central widget
        self.setLayout(layout)
        
        i = 0
        # add the output config filename 
        ################################    
        fnam_label = QtGui.QLabel(self)
        fnam_label.setText('<b>file: </b>'+self.output_filename)
        layout.addWidget(fnam_label, i, 0, 1, 2)
        i += 1
        
        # make labels for groups and labels / lineedits for key / values
        self.group_labels, self.labels_lineedits = self.make_labels_lineedits_from_dict(params, ignore_group = 'help')
        
        # add them to the layout 
        hboxs = []
        for ll, gw in zip(self.labels_lineedits.keys(), self.group_labels) :
            #layout.addWidget(gw)
            layout.addWidget(gw, i, 0, 1, 2)
            i += 1
            for key in self.labels_lineedits[ll].keys():
                layout.addWidget(self.labels_lineedits[ll][key]['label'], i, 0, 1, 1)
                layout.addWidget(self.labels_lineedits[ll][key]['lineedit'], i, 1, 1, 1)
                i+=1
                
                # update the output params dict if a parameter is edited
                self.labels_lineedits[ll][key]['lineedit'].editingFinished.connect(self.update_dict)
        
        self.save_button = QtGui.QPushButton('Save', self)
        self.save_button.clicked.connect(self.write_file)
        self.save_button.setEnabled(False)
        layout.addWidget(self.save_button, i, 0, 1, 2)
        i+=1
        
        
    def update_dict(self):
        for group in self.labels_lineedits.keys():
            for key in self.labels_lineedits[group].keys():
                if self.params[group][key] != str(self.labels_lineedits[group][key]['lineedit'].text().strip()):
                    self.params[group][key] = str(self.labels_lineedits[group][key]['lineedit'].text().strip())
                    self.save_button.setEnabled(True)
    
    def write_file(self):
        with open(self.output_filename, 'w') as f:
            for group in self.params.keys():
                f.write('['+group+']' + '\n')
                
                for key in self.params[group].keys():
                    out_str = key
                    out_str = out_str + ' = '
                    out_str = out_str + str(self.params[group][key]).strip()
                    f.write( out_str + '\n')
        self.save_button.setEnabled(False)
    
    def make_labels_lineedits_from_dict(self, params, ignore_group = 'help'):
        """
        converts the dictionary params to a dictionary containing QT labels and lineedits in the same structure.
        """
        labels_lineedits = OrderedDict()
        group_labels     = []
        for group in params.keys():
            if group == ignore_group :
                continue
            # add a label for the group
            group_labels.append( QtGui.QLabel() )
            group_labels[-1].setText('<b>'+group+'</b>')
            
            labels_lineedits[group] = OrderedDict()
            # add the labels and line edits
            for key in params[group].keys():
                labels_lineedits[group][key] = {}
                labels_lineedits[group][key]['label'] = QtGui.QLabel()
                labels_lineedits[group][key]['label'].setText(key)
                
                labels_lineedits[group][key]['lineedit'] = QtGui.QLineEdit()
                labels_lineedits[group][key]['lineedit'].setText(str(params[group][key]))
                
                labels_lineedits[group][key]['help'] = None
                # see if there is help for this entry
                if 'help' in params :
                    h = group + '.' + key
                    if h in params['help']:
                        print('setting tooltip:',params['help'][h])
                        labels_lineedits[group][key]['help'] = params['help'][h]
                        labels_lineedits[group][key]['label'].setToolTip(params['help'][h].strip("'\""))
        return group_labels, labels_lineedits
        

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL) # allow Control-C
    app = QtGui.QApplication([])
    
    # Qt main window
    Mwin = QtGui.QMainWindow()
    Mwin.setWindowTitle('config editor')
    
    config_widget = Write_config_file_widget('example.ini', 'example_output.ini')
    
    # add the central widget to the main window
    Mwin.setCentralWidget(config_widget)
    
    print('app exec')
    Mwin.show()
    app.exec_()
