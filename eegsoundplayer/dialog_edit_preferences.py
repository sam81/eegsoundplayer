# -*- coding: utf-8 -*-
#   Copyright (C) 2015 Samuele Carcagno <sam.carcagno@gmail.com>
#   This file is part of eegsoundplayer

#    eegsoundplayer is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    eegsoundplayer is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with eegsoundplayer.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
from .pyqtver import*
if pyqtversion == 4:
    from PyQt4 import QtGui, QtCore
    from PyQt4.QtCore import QLocale
    from PyQt4.QtGui import QCheckBox, QComboBox, QDialog, QDialogButtonBox, QDoubleValidator, QFileDialog, QGridLayout, QIntValidator, QLabel, QLineEdit, QPushButton, QTabWidget, QVBoxLayout, QWidget
    QFileDialog.getOpenFileName = QFileDialog.getOpenFileNameAndFilter
    QFileDialog.getOpenFileNames = QFileDialog.getOpenFileNamesAndFilter
    QFileDialog.getSaveFileName = QFileDialog.getSaveFileNameAndFilter
elif pyqtversion == -4:
    from PySide import QtGui, QtCore
    from PySide.QtCore import QLocale
    from PySide.QtGui import QCheckBox, QComboBox, QDialog, QDialogButtonBox, QDoubleValidator, QFileDialog, QGridLayout, QIntValidator, QLabel, QLineEdit, QPushButton, QTabWidget, QVBoxLayout, QWidget
elif pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtCore import QLocale
    from PyQt5.QtGui import QDoubleValidator, QIntValidator
    from PyQt5.QtWidgets import QCheckBox, QComboBox, QDialog, QDialogButtonBox, QFileDialog, QGridLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QVBoxLayout, QWidget

import copy, pickle


class preferencesDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.tmpPref = {}
        self.tmpPref['pref'] = copy.deepcopy(self.parent().prm['pref'])
        self.currLocale = self.parent().prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.OmitGroupSeparator | self.currLocale.RejectGroupSeparator)
        
        self.tabWidget = QTabWidget()
        self.tabWidget.currentChanged.connect(self.tabChanged)
        self.appPrefWidget = QWidget()
        
        #APP PREF
        appPrefGrid = QGridLayout()
        n = 0
        self.startRecWAVButton = QPushButton("Choose Start Recording WAV:", self)
        self.startRecWAVButton.clicked.connect(self.onClickStartRecordingWAV)
        appPrefGrid.addWidget(self.startRecWAVButton, n, 0)

        self.startRecWAV = QLineEdit()
        self.startRecWAV.setText(self.tmpPref['pref']['startRecWAV'])
        appPrefGrid.addWidget(self.startRecWAV, n, 1)
        n = n+1

        self.stopRecWAVButton = QPushButton("Choose Stop Recording WAV:", self)
        self.stopRecWAVButton.clicked.connect(self.onClickStopRecordingWAV)
        appPrefGrid.addWidget(self.stopRecWAVButton, n, 0)

        self.stopRecWAV = QLineEdit()
        self.stopRecWAV.setText(self.tmpPref['pref']['stopRecWAV'])
        appPrefGrid.addWidget(self.stopRecWAV, n, 1)
        n = n+1

        self.markBlockWAVButton = QPushButton("Choose Mark Block Beginning WAV:", self)
        self.markBlockWAVButton.clicked.connect(self.onClickMarkBlockWAV)
        appPrefGrid.addWidget(self.markBlockWAVButton, n, 0)

        self.markBlockWAV = QLineEdit()
        self.markBlockWAV.setText(self.tmpPref['pref']['markBlockWAV'])
        appPrefGrid.addWidget(self.markBlockWAV, n, 1)
        n = n+1

        self.appPrefWidget.setLayout(appPrefGrid)
        


        self.tabWidget.addTab(self.appPrefWidget, self.tr("Applicatio&n"))

        buttonBox = QDialogButtonBox(QDialogButtonBox.Apply|QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.permanentApply)
        
        layout = QVBoxLayout()
        layout.addWidget(self.tabWidget)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

    def onClickStartRecordingWAV(self):
        fName = QFileDialog.getOpenFileName(self, self.tr("Choose WAV file"), '', self.tr("WAV files (*.wav *WAV *Wav);;All Files (*)"))[0]
        if len(fName) > 0: #if the user didn't press cancel
            self.startRecWAV.setText(fName)

    def onClickStopRecordingWAV(self):
        fName = QFileDialog.getOpenFileName(self, self.tr("Choose WAV file"), '', self.tr("WAV files (*.wav *WAV *Wav);;All Files (*)"))[0]
        if len(fName) > 0: #if the user didn't press cancel
            self.stopRecWAV.setText(fName)

    def onClickMarkBlockWAV(self):
        fName = QFileDialog.getOpenFileName(self, self.tr("Choose WAV file"), '', self.tr("WAV files (*.wav *WAV *Wav);;All Files (*)"))[0]
        if len(fName) > 0: #if the user didn't press cancel
            self.markBlockWAV.setText(fName)

    def tryApply(self):
        self.tmpPref['pref']['startRecWAV'] = self.startRecWAV.text()
        self.tmpPref['pref']['stopRecWAV'] = self.stopRecWAV.text()
        self.tmpPref['pref']['markBlockWAV'] = self.markBlockWAV.text()
      
    def revertChanges(self):
        self.startRecWAV.setText(self.tmpPref['pref']['startRecWAV'])
        self.stopRecWAV.setText(self.tmpPref['pref']['stopRecWAV'])
        self.markBlockWAV.setText(self.tmpPref['pref']['markBlockWAV'])
       
    def permanentApply(self):
        self.tryApply()
        self.parent().prm['pref'] = copy.deepcopy(self.tmpPref['pref'])
        f = open(self.parent().prm['prefFile'], 'wb')
        pickle.dump(self.parent().prm['pref'], f)
        f.close()

    def tabChanged(self):
        self.tryApply()
        if self.tmpPref['pref'] != self.parent().prm['pref']:
            conf = applyChanges(self)
            if conf.exec_():
                self.permanentApply()
            else:
                self.tmpPref['pref'] = copy.deepcopy(self.parent().prm['pref'])
                self.revertChanges()
                

class applyChanges(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        grid = QGridLayout()
        n = 0
        label = QLabel(self.tr('There are unsaved changes. Apply Changes?'))
        grid.addWidget(label, n, 1)
        n = n+1
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                     QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        grid.addWidget(buttonBox, n, 1)
        self.setLayout(grid)
        self.setWindowTitle(self.tr("Apply Changes"))
