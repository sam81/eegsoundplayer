#!/usr/bin/python
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
#    along with eegsoundplayer. If not, see <http://www.gnu.org/licenses/>.

import fnmatch, platform, random, signal, subprocess, sys, time
import numpy as np
from tempfile import mkstemp

from eegsoundplayer.pyqtver import*
if pyqtversion == 4:
    from PyQt4 import QtCore, QtGui
    from PyQt4.QtCore import Qt, QEvent, QThread, QDate, QTime, QDateTime
    from PyQt4.QtGui import QAction, QApplication, QCheckBox, QComboBox, QDesktopServices, QDesktopWidget, QDoubleValidator, QFrame, QFileDialog, QGridLayout, QHBoxLayout, QIcon, QIntValidator, QLabel, QLayout, QLineEdit, QMainWindow, QMessageBox, QProgressBar, QScrollArea, QSizePolicy, QSpacerItem, QSplitter, QPushButton, QVBoxLayout, QWhatsThis, QWidget
    QFileDialog.getOpenFileName = QFileDialog.getOpenFileNameAndFilter
    QFileDialog.getOpenFileNames = QFileDialog.getOpenFileNamesAndFilter
    QFileDialog.getSaveFileName = QFileDialog.getSaveFileNameAndFilter
    Signal = QtCore.pyqtSignal
    Slot = QtCore.pyqtSlot
elif pyqtversion == -4:
    import PySide
    from PySide import QtCore, QtGui
    from PySide.QtCore import Qt, QEvent, QThread, Signal, Slot, QDate, QTime, QDateTime
    from PySide.QtGui import QAction, QApplication, QCheckBox, QComboBox, QDesktopServices, QDesktopWidget, QDoubleValidator, QFrame, QFileDialog, QGridLayout, QHBoxLayout, QIcon, QIntValidator, QLabel, QLayout, QLineEdit, QMainWindow, QMessageBox, QProgressBar, QScrollArea, QSizePolicy, QSpacerItem, QSplitter, QPushButton, QVBoxLayout, QWhatsThis, QWidget
elif pyqtversion == 5:
    from PyQt5 import QtCore, QtGui
    from PyQt5.QtCore import Qt, QEvent, QThread, QDate, QTime, QDateTime
    from PyQt5.QtWidgets import QAction, QApplication, QCheckBox, QComboBox, QDesktopWidget, QFrame, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QLayout, QLineEdit, QMainWindow, QMessageBox, QProgressBar, QScrollArea, QSizePolicy, QSpacerItem, QSplitter, QPushButton, QVBoxLayout, QWhatsThis, QWidget
    from PyQt5.QtGui import QDesktopServices, QDoubleValidator, QIcon, QIntValidator
    Signal = QtCore.pyqtSignal
    Slot = QtCore.pyqtSlot
signal.signal(signal.SIGINT, signal.SIG_DFL)

from eegsoundplayer import qrc_resources
from eegsoundplayer.dialog_edit_preferences import*
from eegsoundplayer.global_parameters import*
from eegsoundplayer.sndlib import*
from eegsoundplayer.wavpy import*
from eegsoundplayer._version_info import*
from eegsoundplayer.utilities_open_manual import*


__version__ = eegsoundplayer_version

class EEGSoundPlayer(QMainWindow):
    def __init__(self, parent=None, prm=None):
        QMainWindow.__init__(self, parent)
        self.prm = prm#{}
        self.prm['currentLocale'] = QtCore.QLocale("en_GB")
        self.cw = QFrame()
        self.gridBox = QGridLayout()

        self.menubar = self.menuBar()
        #FILE MENU
        self.fileMenu = self.menubar.addMenu(self.tr('&File'))

        # exitButton = QAction(QIcon(':/exit.svg'), self.tr('Exit'), self)
        # exitButton.setShortcut('Ctrl+Q')
        # exitButton.setStatusTip(self.tr('Exit application'))
        # exitButton.triggered.connect(self.close)
        # self.fileMenu.addAction(exitButton)

        self.openStimListButton = QAction(QIcon.fromTheme("document-open", QIcon(":/document-open")), self.tr("Open Stim. List"), self)
        self.openStimListButton.setStatusTip(self.tr('Open Stim. List'))
        self.openStimListButton.triggered.connect(self.onClickOpenStimListButton)

        self.openLogFileButton = QAction(QIcon.fromTheme("document-open", QIcon(":/document-open")), self.tr('Open Log File'), self)
        self.openLogFileButton.setStatusTip(self.tr('Open Log File'))
        self.openLogFileButton.triggered.connect(self.onClickOpenLogFileButton)

        # self.openStdoutFileButton = QAction(QIcon.fromTheme("document-open", QIcon(":/document-open")), self.tr('Open stdout File'), self)
        # self.openStdoutFileButton.setStatusTip(self.tr('Open stdout File'))
        # self.openStdoutFileButton.triggered.connect(self.onClickOpenStdoutFileButton)

        self.openStderrFileButton = QAction(QIcon.fromTheme("document-open", QIcon(":/document-open")), self.tr('Open stderr File'), self)
        self.openStderrFileButton.setStatusTip(self.tr('Open stderr File'))
        self.openStderrFileButton.triggered.connect(self.onClickOpenStderrFileButton)

        self.fileMenu.addAction(self.openStimListButton)
        self.fileMenu.addAction(self.openLogFileButton)
        #self.fileMenu.addAction(self.openStdoutFileButton)
        self.fileMenu.addAction(self.openStderrFileButton)

        #EDIT MENU
        self.editMenu = self.menubar.addMenu(self.tr('&Edit'))
        self.openLogFileButton = QAction(QIcon.fromTheme("document-open", QIcon(":/document-open")), self.tr('Open Log File'), self)
        self.editPrefAction = QAction(self.tr('Preferences'), self)
        self.editMenu.addAction(self.editPrefAction)
        self.editPrefAction.triggered.connect(self.onEditPref)
        
        #HELP MENU
        self.helpMenu = self.menubar.addMenu(self.tr('&Help'))

        self.onShowManualHTMLAction = QAction(self.tr('Manual (html)'), self)
        self.helpMenu.addAction(self.onShowManualHTMLAction)
        self.onShowManualHTMLAction.triggered.connect(onShowManualHTML)

        self.onShowManualPDFAction = QAction(self.tr('Manual (pdf)'), self)
        self.helpMenu.addAction(self.onShowManualPDFAction)
        self.onShowManualPDFAction.triggered.connect(onShowManualPDF)
        
        self.onAboutAction = QAction(self.tr('About eegsoundplayer'), self)
        self.helpMenu.addAction(self.onAboutAction)
        self.onAboutAction.triggered.connect(self.onAbout)
        
        n = 0
        ###########
        ## SOUND PLAY BUTTON
        self.soundPlayButton = QPushButton("Play", self)
        self.soundPlayButton.clicked.connect(self.onClickSoundPlayButton)
        self.soundPlayButton.setIcon(QtGui.QIcon.fromTheme("media-playback-start", QIcon(":/media-playback-start")))
        self.gridBox.addWidget(self.soundPlayButton, n, 0)
        ###########
        ## LOAD STIM LIST BUTTON
        self.loadStimListButton = QPushButton("Load Stim. List", self)
        self.loadStimListButton.setIcon(QIcon.fromTheme("document-open", QIcon(":/document-open")))
        self.loadStimListButton.clicked.connect(self.onClickLoadStimListButton)
        self.gridBox.addWidget(self.loadStimListButton, n, 1)

        n=n+1
        self.saveLogButton = QPushButton(self.tr("Choose Log File"), self)
        self.saveLogButton.clicked.connect(self.onClickSaveLogButton)
        self.saveLogButton.setIcon(QIcon.fromTheme("document-save", QIcon(":/document-save")))
        self.saveLogButton.setToolTip(self.tr("Choose file to save results"))
        self.gridBox.addWidget(self.saveLogButton, n, 0)
        
        self.resetButton = QPushButton("Reset", self)
        self.resetButton.clicked.connect(self.onClickResetButton)
        self.gridBox.addWidget(self.resetButton, n, 1)

        n = n+1
        self.soundCheckButton = QPushButton("Sound Check", self)
        self.soundCheckButton.setIcon(QtGui.QIcon.fromTheme("media-playback-start", QIcon(":/media-playback-start")))
        self.soundCheckButton.clicked.connect(self.onClickSoundCheckButton)
        self.gridBox.addWidget(self.soundCheckButton, n, 1)

        n = n+1
        self.subjIDLabel = QLabel("Participant ID:", self)
        self.gridBox.addWidget(self.subjIDLabel, n, 0)
        self.subjID = QLineEdit()
        self.subjID.setText("")
        self.gridBox.addWidget(self.subjID, n, 1)

        n = n+1
        self.ISITypeLabel =  QLabel("ISI Type:", self)
        self.gridBox.addWidget(self.ISITypeLabel, n, 0)
        self.ISITypeChooser = QComboBox()
        self.ISITypeChooser.addItems(["Fixed", "Random Uniform"])
        self.ISITypeChooser.setCurrentIndex(0)
        self.gridBox.addWidget(self.ISITypeChooser, n, 1)
        self.ISITypeChooser.activated[str].connect(self.onISITypeChooseChange)


        n = n+1
        self.ISILabel = QLabel("ISI (ms):", self)
        self.gridBox.addWidget(self.ISILabel, n, 0)
        self.ISIBox = QLineEdit()
        self.ISIBox.setText('500')
        self.ISIBox.setValidator(QIntValidator(self))
        self.gridBox.addWidget(self.ISIBox, n, 1)

        n = n+1
        self.ISIMinLabel = QLabel("ISI Min. (ms):", self)
        self.gridBox.addWidget(self.ISIMinLabel, n, 0)
        self.ISIMinLabel.hide()
        self.ISIMinBox = QLineEdit()
        self.ISIMinBox.setText('300')
        self.ISIMinBox.setValidator(QIntValidator(self))
        self.gridBox.addWidget(self.ISIMinBox, n, 1)
        self.ISIMinBox.hide()

        n = n+1
        self.ISIMaxLabel = QLabel("ISI Max. (ms):", self)
        self.gridBox.addWidget(self.ISIMaxLabel, n, 0)
        self.ISIMaxLabel.hide()
        self.ISIMaxBox = QLineEdit()
        self.ISIMaxBox.setText('500')
        self.ISIMaxBox.setValidator(QIntValidator(self))
        self.gridBox.addWidget(self.ISIMaxBox, n, 1)
        self.ISIMaxBox.hide()

        n = n+1
        self.prevBlockButton = QPushButton("Previous", self)
        self.prevBlockButton.clicked.connect(self.onClickPrevBlockButton)
        self.prevBlockButton.setIcon(QIcon.fromTheme("go-previous", QIcon(":/go-previous")))
        self.prevBlockButton.setToolTip("Move to previous block")
        self.gridBox.addWidget(self.prevBlockButton, n, 0)

        self.nextBlockButton = QPushButton("Next", self)
        self.nextBlockButton.clicked.connect(self.onClickNextBlockButton)
        self.nextBlockButton.setIcon(QIcon.fromTheme("go-next", QIcon(":/go-next")))
        self.nextBlockButton.setToolTip("Move to next block")
        self.gridBox.addWidget(self.nextBlockButton, n, 1)

        n = n+1
        self.currentBlockLabel = QLabel("Block Label: ")
        self.gridBox.addWidget(self.currentBlockLabel, n, 0)
        
        self.storedBlocksLabel = QLabel("Stored Blocks: 0")
        self.gridBox.addWidget(self.storedBlocksLabel, n, 1)

        n = n+1
        self.currentBlockPositionLabel = QLabel("Block Position: ")
        self.gridBox.addWidget(self.currentBlockPositionLabel, n, 0)
        
        n = n+1
        self.shuffleBlocksCheckBox = QCheckBox(self.tr('Shuffle Blocks'))
        self.shuffleTrialsCheckBox = QCheckBox(self.tr('Shuffle Trials'))
        self.gridBox.addWidget(self.shuffleBlocksCheckBox, n, 0)
        self.gridBox.addWidget(self.shuffleTrialsCheckBox, n, 1)

        self.gauge = QProgressBar(self)
        self.gauge.setRange(0, 100)
        self.blockGauge = QProgressBar(self)

        #self.ETABlockTF = QLabel("")

        self.vBox = QVBoxLayout()
        self.vBox.addLayout(self.gridBox)
        self.vBox.addWidget(self.gauge)
        self.vBox.addWidget(self.blockGauge)
        #self.vBox.addWidget(self.ETABlockTF)

        self.cw.setLayout(self.vBox)
        self.cw.layout().setSizeConstraint(QLayout.SetFixedSize)
        self.setCentralWidget(self.cw)
        self.setWindowTitle('EEG Sound Player')
        self.statusBar().showMessage("No Stimulus List Loaded")

        self.playThread = threadedPlayer(self)
        self.playThread.progress.connect(self.updateGauge)
        self.playThread.blockCompleted.connect(self.moveToNextBlock)
        self.currentCount = 0
        self.currentBlock = 1
        self.blockLabels = ['']

        if platform.system() == "Linux":
            self.playCmdString = "aplay "
        elif platform.system() == 'Darwin':
            self.playCmdString = "afplay "

        self.prm["sampRate"] = 48000
        self.prm["maxLevel"] = 101
        self.prm["soundCheckRunning"] = False
        self.nBlocks = 0
        self.totalCount = 0
        self.runningBlock = False
        self.playing = False
        self.stimListLoaded = False
        self.finishedSession = False
        self.logFileIsOpen = False
        self.sessionStartTime = None
        self.show()
        
    def updateGauge(self, val):
        self.gauge.setValue(val)
        self.blockElapsedTime = time.time() - self.blockStartTime
        self.blockETA = (100*self.blockElapsedTime)/val - self.blockElapsedTime
        bl_minutes = int(self.blockETA // 60)
        bl_seconds = int(self.blockETA - (bl_minutes * 60))
        if bl_minutes > 0:
            blockETAStr =  ('%s min %s sec' % (bl_minutes, bl_seconds))
        else:
            blockETAStr =  ('%s sec' % (bl_seconds))

        self.gauge.setFormat(str(val)+"%"+ " - ETA: "+ blockETAStr)

        # pcBlocksCompleted = (self.currentBlock-1)/self.nBlocks*100 + (val/100)*(1/self.nBlocks*100)
        # self.sessionElapsedTime = time.time() - self.sessionStartTime
        # self.sessionETA = ((100*self.sessionElapsedTime)/pcBlocksCompleted - self.sessionElapsedTime )

        # sess_minutes = int(self.sessionETA // 60)
        # sess_seconds = int(self.sessionETA - (sess_minutes * 60))
        # if sess_minutes > 0:
        #     sessionETAStr =  ('%s min %s sec' % (sess_minutes, sess_seconds))
        # else:
        #     sessionETAStr =  ('%s sec' % (sess_seconds))
        # self.blockGauge.setFormat(("Blocks Completed" +  ': ' + str(self.currentBlock-1) + '/' + str(self.nBlocks) + " - ETA: " + sessionETAStr))
        self.updateBlockGauge()

    def updateBlockGauge(self):
        val = self.gauge.value()
        try:
            pcBlocksCompleted = (self.currentBlock-1)/self.nBlocks*100 + (val/100)*(1/self.nBlocks*100)
        except:
           pcBlocksCompleted = 0

        if pcBlocksCompleted > 0 and self.sessionStartTime != None:
            self.sessionElapsedTime = time.time() - self.sessionStartTime
            self.sessionETA = ((100*self.sessionElapsedTime)/pcBlocksCompleted - self.sessionElapsedTime )

            sess_minutes = int(self.sessionETA // 60)
            sess_seconds = int(self.sessionETA - (sess_minutes * 60))
            if sess_minutes > 0:
                sessionETAStr =  ('%s min %s sec' % (sess_minutes, sess_seconds))
            else:
                sessionETAStr =  ('%s sec' % (sess_seconds))
            self.blockGauge.setFormat(("Blocks Completed" +  ': ' + str(self.currentBlock-1) + '/' + str(self.nBlocks) + " - ETA: " + sessionETAStr))
        
    def updateStatus(self):
        self.blockGauge.setRange(0, self.nBlocks)
        self.blockGauge.setValue(self.currentBlock-1)
        self.blockGauge.setFormat("Blocks Completed" +  ': ' + str(self.currentBlock-1) + '/' + str(self.nBlocks))
        self.currentBlockLabel.setText("Block Label: " + self.blockLabels[self.currentBlock-1])
        self.currentBlockPositionLabel.setText("Block Position: " + str(self.currentBlock))
        self.storedBlocksLabel.setText("Stored Blocks: " + str(self.nBlocks))
        if self.stimListLoaded == True:
            self.totalCount = len(self.trialList[self.blockLabels.index('B'+str(self.currentBlock))])
        self.updateBlockGauge()

    def onClickResetButton(self):
        if self.stimListLoaded == False:
            return
        if self.finishedSession == False:
            reply = QMessageBox.question(self, 'Message', "Session currently running, are you sure you want to reset?", QMessageBox.Yes | 
                                               QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.No:
                return
        self.resetSession()
        
    def resetSession(self):
        self.playThread.terminate()
        self.finishedSession = False
        self.runningBlock = False
        self.playing = False

        try:
            self.logFileHandle.close()
        except:
            pass
        self.logFileIsOpen = False
    
        if self.stimListLoaded:
            self.blockPositions = list(range(self.nBlocks))

        self.statusBar().showMessage("Paused")
        self.soundPlayButton.setText("Play")
        self.soundPlayButton.setIcon(QtGui.QIcon.fromTheme("media-playback-start", QIcon(":/media-playback-start")))
        
        self.currentBlock = 1
        self.currentCount = 0
        self.gauge.setValue(0)
        self.gauge.setFormat(str(0)+"%"+ " - ETA: --")
        self.updateStatus()

     
            
    def onClickSoundPlayButton(self):
        if self.stimListLoaded == False:# or self.finishedSession == True:
            ret = QMessageBox.warning(self, self.tr("Warning"),
                                      "No stimulus list is loaded. Would you like to load one?",
                                      QMessageBox.Yes | QMessageBox.No)
            if ret == QMessageBox.Yes:
                self.onClickLoadStimListButton()
            else:
                return
        if self.finishedSession == True:
            ret = QMessageBox.warning(self, self.tr("Warning"),
                                      "Session finished. Please, click the reset button to start a new session.",
                                      QMessageBox.Ok)
            return
        if self.logFileIsOpen == False:
            self.onClickSaveLogButton()

        
        
        if self.currentBlock == 1:
            if self.shuffleBlocksCheckBox.isChecked() == True:
                random.shuffle(self.blockLabels)
            if self.shuffleTrialsCheckBox.isChecked() == True:
                for bl in range(self.nBlocks):
                    random.shuffle(self.trialList[bl])
            self.sessionStartTime = time.time()
            self.totalCount = len(self.trialList[self.blockLabels.index('B'+str(self.currentBlock))])
            self.updateStatus()
            
        self.blockStartTime = time.time()
        if self.sessionStartTime == None:
            self.sessionStartTime = time.time()
            
        self.runningBlock = True
        if self.playing == False:
            if self.prm["pref"]["startRecWAV"] != "":
                subprocess.call(self.playCmdString + self.prm["pref"]["startRecWAV"], shell=True)
                time.sleep(0.5)
            self.playing = True
            self.statusBar().showMessage("Playing")
            self.soundPlayButton.setIcon(QtGui.QIcon.fromTheme("media-playback-pause", QIcon(":/media-playback-pause")))
            self.soundPlayButton.setText("Pause")
            self.playThread.playThreadedSound()
        else:
            self.playing = False
            self.statusBar().showMessage("Paused")
            self.soundPlayButton.setIcon(QtGui.QIcon.fromTheme("media-playback-start", QIcon(":/media-playback-start")))
            self.soundPlayButton.setText("Play")
            self.playThread.terminate()
            if 'sleepBeforeStop' in self.prm:
                time.sleep(self.prm['sleepBeforeStop']/1000)
            else:
                time.sleep(1)
            if self.prm["pref"]["stopRecWAV"] != "":
                subprocess.call(self.playCmdString + self.prm["pref"]["stopRecWAV"], shell=True)
                #time.sleep(0.5)

    def onClickSoundPauseButton(self):
        self.playThread.terminate()

    def moveToNextBlock(self):
        self.runningBlock = False
        self.playing = False
        self.logFileHandle.flush()
        self.statusBar().showMessage("Idle")
        self.soundPlayButton.setIcon(QtGui.QIcon.fromTheme("media-playback-start", QIcon(":/media-playback-start")))
        self.soundPlayButton.setText("Play")
       
        if self.currentBlock < self.nBlocks:
            self.gauge.setValue(0)
            self.currentCount = 0
            self.currentBlock = self.currentBlock + 1
            self.totalCount = len(self.trialList[self.blockLabels.index('B'+str(self.currentBlock))])
            self.updateStatus()
        else:
            self.finishedSession = True
            self.statusBar().showMessage("Finished Session")
            self.blockGauge.setValue(self.nBlocks)
            self.blockGauge.setFormat("Blocks Completed" +  ': ' + str(self.currentBlock) + '/' + str(self.nBlocks))
            self.logFileHandle.close()
            #self.stdoutFileHandle.close()
            self.stderrFileHandle.close()
            self.logFileIsOpen = False

    def onClickNextBlockButton(self):
        if self.stimListLoaded == False or self.runningBlock == True:
            return
  
        self.finishedSession = False
        if self.currentBlock < self.nBlocks:
            self.moveToBlock(self.currentBlock+1)
        else:
            self.moveToBlock(1)
            
    def onClickPrevBlockButton(self):
        if self.stimListLoaded == False or self.runningBlock == True:
            return

        self.finishedSession = False
        if self.currentBlock > 1:
            self.moveToBlock(self.currentBlock-1)
        else:
            self.moveToBlock(self.nBlocks)
            
    def moveToBlock(self, blockNumber):
        self.currentCount = 0
        self.currentBlock = blockNumber
        self.gauge.setValue(0)
        self.updateStatus()
        
    def onClickLoadStimListButton(self):
        fName = QFileDialog.getOpenFileName(self, self.tr("Choose parameters file to load"), '', self.tr("text files (*.txt *TXT *Txt);;All Files (*)"))[0]
        if len(fName) > 0: #if the user didn't press cancel
            self.resetSession()
            self.stimListFilePath = fName
            fStream = open(fName, 'r')
            allLines = fStream.readlines()
            fStream.close()
            self.nBlocks = sum(x == "++++++++++\n" for x in allLines)
            idxStart = [i+1 for i, x in enumerate(allLines) if x == "++++++++++\n"]
            idxStop = [i for i, x in enumerate(allLines) if x == "----------\n"]
            self.trialList = [allLines[idxStart[i]:idxStop[i]] for i in range(self.nBlocks)]
            for nl in range(len(self.trialList)):
                self.trialList[nl] = [self.trialList[nl][i].strip() for i in range(len(self.trialList[nl]))]
            self.blockPositions = list(range(self.nBlocks))
            self.blockLabels = ["B" + str(bl+1) for bl in self.blockPositions]

            for ln in allLines:
                if ln[0:14] == "Shuffle Blocks" and ln.split(":")[1].strip() == "True":
                    self.shuffleBlocksCheckBox.setChecked(True)
                if ln[0:14] == "Shuffle Trials" and ln.split(":")[1].strip() == "True":
                    self.shuffleTrialsCheckBox.setChecked(True)
                if ln[0:3] == "ISI":
                    if len(ln.split(":")[1].split("-")) == 1:
                        self.ISITypeChooser.setCurrentIndex(0)
                        self.onISITypeChooseChange("Fixed")
                        ISI = ln.split(":")[1].strip()
                        self.ISIBox.setText(ISI)
                    else:
                        self.ISITypeChooser.setCurrentIndex(1)
                        self.onISITypeChooseChange("Random Uniform")
                        ISIMin = ln.split(":")[1].split("-")[0].strip()
                        ISIMax = ln.split(":")[1].split("-")[1].strip()
                        self.ISIMinBox.setText(ISIMin)
                        self.ISIMaxBox.setText(ISIMax)
                if ln[0:17] == "Sleep Before Stop":
                    self.prm['sleepBeforeStop'] = int(ln.split(":")[1].strip())
            self.stimListLoaded = True
            self.statusBar().showMessage("Ready")
            self.totalCount = len(self.trialList[0])
            self.updateStatus()

    def onClickSaveLogButton(self):
        ftow = QFileDialog.getSaveFileName(self, self.tr('Choose file to write log'), "", self.tr('All Files (*)'), "", QFileDialog.DontConfirmOverwrite)[0]
        if len(ftow) > 0:
            if fnmatch.fnmatch(ftow, '*.txt') == False:
                ftow = ftow + '.txt'
            self.prm["logFilePath"] = ftow
            self.logFileHandle = open(ftow, 'a')
            self.logFileIsOpen = True
            
            rootFilePath = "".join(ftow.split(".")[0:len(ftow.split("."))-1])
            #self.prm["stdoutFilePath"] = rootFilePath + "_stdout" + ".txt"
            #self.stdoutFileHandle = open(self.prm["stdoutFilePath"], "a")
            self.prm["stderrFilePath"] = rootFilePath + "_stderr" + ".txt"
            self.stderrFileHandle = open(self.prm["stderrFilePath"], "a")
                
                
    def onISITypeChooseChange(self, ISIType):
        if ISIType == "Fixed":
            self.ISILabel.show()
            self.ISIBox.show()
            self.ISIMinLabel.hide()
            self.ISIMaxLabel.hide()
            self.ISIMinBox.hide()
            self.ISIMaxBox.hide()
        elif ISIType == "Random Uniform":
            self.ISIMinLabel.show()
            self.ISIMaxLabel.show()
            self.ISIMinBox.show()
            self.ISIMaxBox.show()
            self.ISILabel.hide()
            self.ISIBox.hide()

    def onClickOpenStimListButton(self):
        if self.stimListLoaded == True:
            fileToOpen = self.stimListFilePath
            QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))
        else:
            ret = QMessageBox.information(self, self.tr("message"),
                                                self.tr("No stimulus list has been loaded yet."),
                                                QMessageBox.Ok)
    def onClickOpenLogFileButton(self):
        if "logFilePath" in self.prm:
            fileToOpen = self.prm["logFilePath"]
            QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))
        else:
            ret = QMessageBox.information(self, self.tr("message"),
                                                self.tr("No log file has been selected yet."),
                                                QMessageBox.Ok)

    def onClickOpenStdoutFileButton(self):
        if "stdoutFilePath" in self.prm:
            fileToOpen = self.prm["stdoutFilePath"]
            QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))
        else:
            ret = QMessageBox.information(self, self.tr("message"),
                                                self.tr("No stdout file has been selected yet. \nChoose a Log file in order to select the stderr file."),
                                                QMessageBox.Ok)

    def onClickOpenStderrFileButton(self):
        if "stderrFilePath" in self.prm:
            fileToOpen = self.prm["stderrFilePath"]
            QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))
        else:
            ret = QMessageBox.information(self, self.tr("message"),
                                                self.tr("No stderr file has been selected yet. \nChoose a Log file in order to select the stderr file."),
                                                QMessageBox.Ok)

    def onClickSoundCheckButton(self):
        if self.prm["soundCheckRunning"] == False:
            self.prm["soundCheckRunning"] = True
            self.soundCheckButton.setIcon(QtGui.QIcon.fromTheme("media-playback-pause", QIcon(":/media-playback-stop")))
            self.soundCheckButton.setText("Stop Sound Check")
            snd = self.makeSoundCheckWAV()
            (hnl, self.soundCheckWAVFilePath) = mkstemp("tmp_snd.wav")
            wavwrite(snd, self.prm['sampRate'], 32, self.soundCheckWAVFilePath)
            self.playThread2 = threadedPlayer2(self)
            self.playThread2.playThreadedSound(self.soundCheckWAVFilePath)
        else:
            self.playThread2.terminate()
            self.soundCheckButton.setIcon(QtGui.QIcon.fromTheme("media-playback-start", QIcon(":/media-playback-start")))
            self.soundCheckButton.setText("Sound Check")
            self.prm["soundCheckRunning"] = False
                 
    def makeSoundCheckWAV(self):
        G= 196
        Eb= 155.56
        F= 174.61
        D = 146.83
        tUnit = 250
        ramp = 25
        level = 80
        channel = "Both"
        lowHarm = 2
        highHarm = 2
        
        
        thisSnd = complexTone(G, "Sine", lowHarm, highHarm, 0, level, tUnit, ramp, channel, self.prm['sampRate'], self.prm['maxLevel'])
        p1 = concatenate((thisSnd, thisSnd), axis=0)
        p1 = concatenate((p1, thisSnd), axis=0)

        p2 = complexTone(Eb, "Sine", lowHarm, highHarm, 0, level, tUnit*4, ramp, channel, self.prm['sampRate'], self.prm['maxLevel'])
        p3 = makeSilence(tUnit+ramp*2, self.prm['sampRate'])
        thisSnd = complexTone(F, "Sine", lowHarm, highHarm, 0, level, tUnit, ramp, channel, self.prm['sampRate'], self.prm['maxLevel'])
        p4 = concatenate((thisSnd, thisSnd), axis=0)
        p4 = concatenate((p4, thisSnd), axis=0)

        p5 = complexTone(D, "Sine", lowHarm, highHarm, 0, level, tUnit*4, ramp, channel, self.prm['sampRate'], self.prm['maxLevel'])
        snd = concatenate((p1, p2), axis=0)
        snd = concatenate((snd, p3), axis=0)
        snd = concatenate((snd, p4), axis=0)

        snd = concatenate((snd, p5), axis=0)
        
        return snd

    def onEditPref(self):
        dialog = preferencesDialog(self)
        if dialog.exec_():
            dialog.permanentApply()

    def onAbout(self):
        if pyqtversion in [4,5]:
            qt_compiled_ver = QtCore.QT_VERSION_STR
            qt_runtime_ver = QtCore.qVersion()
            qt_pybackend_ver = QtCore.PYQT_VERSION_STR
            qt_pybackend = "PyQt"
        elif pyqtversion == -4:
            qt_compiled_ver = QtCore.__version__
            qt_runtime_ver = QtCore.qVersion()
            qt_pybackend_ver = PySide.__version__
            qt_pybackend = "PySide"
        QMessageBox.about(self, self.tr("About eegsoundplayer"),
                                self.tr("""<b>eegsoundplayer - EEG Sound Player</b> <br>
                                - version: {0}; <br>
                                - build date: {1} <br>
                                <p> Copyright &copy; 2015 Samuele Carcagno. <a href="mailto:sam.carcagno@gmail.com">sam.carcagno@gmail.com</a> 
                                All rights reserved. <p>
                This program is free software: you can redistribute it and/or modify
                it under the terms of the GNU General Public License as published by
                the Free Software Foundation, either version 3 of the License, or
                (at your option) any later version.
                <p>
                This program is distributed in the hope that it will be useful,
                but WITHOUT ANY WARRANTY; without even the implied warranty of
                MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
                GNU General Public License for more details.
                <p>
                You should have received a copy of the GNU General Public License
                along with this program.  If not, see <a href="http://www.gnu.org/licenses/">http://www.gnu.org/licenses/</a>
                <p>Python {2} - {3} {4} compiled against Qt {5}, and running with Qt {6} on {7}""").format(__version__, eegsoundplayer_builddate, platform.python_version(), qt_pybackend, qt_pybackend_ver, qt_compiled_ver, qt_runtime_ver, platform.system()))
         
class threadedPlayer(QThread):
    progress = Signal(int)
    blockCompleted = Signal()
    def __init__(self, parent):
        QThread.__init__(self, parent)
        
    def playThreadedSound(self):
        self.start()
    def run(self):
        while self.parent().currentCount < self.parent().totalCount and self.parent().runningBlock == True:
            if self.parent().currentCount == 0:
                # if self.prm["pref"]["startRecWAV"] != "":
                #     subprocess.call(self.parent().playCmdString + self.prm["pref"]["startRecWAV"], shell=True)
                #     time.sleep(0.5)
                if self.parent().prm["pref"]["markBlockWAV"] != "":
                    subprocess.call(self.parent().playCmdString + self.parent().prm["pref"]["markBlockWAV"], shell=True)
                    time.sleep(0.5)
            print("Playing: " + self.parent().trialList[self.parent().blockLabels.index('B'+str(self.parent().currentBlock))][self.parent().currentCount])
            filePath = self.parent().trialList[self.parent().blockLabels.index('B'+str(self.parent().currentBlock))][self.parent().currentCount]
            #subprocess.call(self.parent().playCmdString + filePath, stdout=self.parent().stdoutFileHandle, stderr=self.parent().stderrFileHandle, shell=True)
            subprocess.call(self.parent().playCmdString + filePath, stderr=self.parent().stderrFileHandle, shell=True)
            if self.parent().ISITypeChooser.currentText() == "Fixed":
                ISI = int(self.parent().ISIBox.text())
            else:
                ISI = random.uniform(int(self.parent().ISIMinBox.text()), int(self.parent().ISIMaxBox.text()))
            time.sleep(ISI/1000)
            currDate = QDate.toString(QDate.currentDate(), self.parent().prm["currentLocale"].dateFormat(self.parent().prm["currentLocale"].ShortFormat)) 
            currTime = QTime.toString(QTime.currentTime())#, self.parent().prm["currentLocale"].timeFormat(self.parent().prm["currentLocale"].ShortFormat)) 
            self.parent().logFileHandle.write(filePath + ";" + self.parent().blockLabels[self.parent().currentBlock-1] + ";" + self.parent().subjID.text() + ";" + currDate + ";" + currTime + "\n")
            
            self.parent().currentCount = self.parent().currentCount + 1

            pcTot = self.parent().currentCount / self.parent().totalCount * 100
            self.progress.emit(int(pcTot))
            if self.parent().currentCount == self.parent().totalCount:
                self.blockCompleted.emit()
                if self.parent().prm["pref"]["stopRecWAV"] != "":
                    subprocess.call(self.parent().playCmdString + self.parent().prm["pref"]["stopRecWAV"], shell=True)


class threadedPlayer2(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
    def playThreadedSound(self, filePath):
        self.filePath = filePath
        self.start()
    def run(self):
        while True:
            subprocess.call(self.parent().playCmdString + self.filePath, shell=True)
            time.sleep(0.5)

def main():
    prm = {}
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon.fromTheme("media-playback-start", QIcon(":/media-playback-start")))
    prm = get_prefs(prm)
    prm = global_parameters(prm)
    ex = EEGSoundPlayer(prm=prm)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main() 
