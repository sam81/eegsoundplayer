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
    from PyQt4.QtGui import QDesktopServices
elif pyqtversion == -4:
    from PySide import QtGui, QtCore
    from PySide.QtGui import QDesktopServices
elif pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtGui import QDesktopServices
    
import os

def onShowManualPDF(self):
    fileToOpen = os.path.abspath(os.path.dirname(__file__)) + '/doc/_build/latex/eegsoundplayer.pdf'
    QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))
    return

def onShowManualHTML(self):
    fileToOpen = os.path.abspath(os.path.dirname(__file__)) + '/doc/_build/html/index.html'
    QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))
    return


