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
import matplotlib
matplotlib.rcParams['path.simplify'] = False

from .pyqtver import*
if pyqtversion == 4:
    from PyQt4 import QtGui, QtCore
    from PyQt4.QtGui import QApplication, QColor
    matplotlib.rcParams['backend'] = "Qt4Agg"
    matplotlib.rcParams['backend.qt4'] = "PyQt4"
elif pyqtversion == -4:
    from PySide import QtGui, QtCore
    from PySide.QtGui import QApplication, QColor
    matplotlib.rcParams['backend'] = "Qt4Agg"
    matplotlib.rcParams['backend.qt4'] = "PySide"
elif pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtGui import QColor
    from PyQt5.QtWidgets import QApplication
    matplotlib.rcParams['backend'] = "Qt5Agg"

import platform, os, pickle


def global_parameters(prm):

    return prm
  

def def_prefs(prm):
    prm["pref"] = {}

    prm['pref']['startRecWAV'] = ""
    prm['pref']['stopRecWAV'] = ""
    prm['pref']['markBlockWAV'] = "" #trigger marking the beginning of a block

    return prm


def get_prefs(prm):
    prm = def_prefs(prm)
    prm['prefFile'] = os.path.expanduser("~") +'/.config/eegsoundplayer/preferences'

    if os.path.exists(os.path.expanduser("~") +'/.config/') == False:
        os.mkdir(os.path.expanduser("~") +'/.config/')
    if os.path.exists(os.path.expanduser("~") +'/.config/eegsoundplayer/') == False:
        os.mkdir(os.path.expanduser("~") +'/.config/eegsoundplayer/')
    if os.path.exists(prm['prefFile']):
        fIn = open(prm['prefFile'], 'rb')
        prm['tmp'] = pickle.load(fIn)
        fIn.close()
        for k in prm['pref'].keys():
            if k in prm['tmp']:
                prm['pref'][k] = prm['tmp'][k]
    return prm
