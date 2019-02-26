# -*- coding: utf-8 -*-
#   Copyright (C) 2015-2019 Samuele Carcagno <sam.carcagno@gmail.com>
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

# from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
# from .pyqtver import*
# if pyqtversion == 4:
#     from PyQt4 import QtGui, QtCore
#     from PyQt4.QtCore import QLocale
#     from PyQt4.QtGui import QCheckBox, QComboBox, QDialog, QDialogButtonBox, QDoubleValidator, QFileDialog, QGridLayout, QIntValidator, QLabel, QLineEdit, QPushButton, QTabWidget, QVBoxLayout, QWidget
#     QFileDialog.getOpenFileName = QFileDialog.getOpenFileNameAndFilter
#     QFileDialog.getOpenFileNames = QFileDialog.getOpenFileNamesAndFilter
#     QFileDialog.getSaveFileName = QFileDialog.getSaveFileNameAndFilter
# elif pyqtversion == -4:
#     from PySide import QtGui, QtCore
#     from PySide.QtCore import QLocale
#     from PySide.QtGui import QCheckBox, QComboBox, QDialog, QDialogButtonBox, QDoubleValidator, QFileDialog, QGridLayout, QIntValidator, QLabel, QLineEdit, QPushButton, QTabWidget, QVBoxLayout, QWidget
# elif pyqtversion == 5:
#     from PyQt5 import QtGui, QtCore
#     from PyQt5.QtCore import QLocale
#     from PyQt5.QtGui import QDoubleValidator, QIntValidator
#     from PyQt5.QtWidgets import QCheckBox, QComboBox, QDialog, QDialogButtonBox, QFileDialog, QGridLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QVBoxLayout, QWidget

# import copy, pickle
import os

def get_test_sound_path():
    testSoundPath = os.path.abspath(os.path.dirname(__file__)) + '/sounds/left_right_tone_test_48000Hz.wav'
    return testSoundPath
