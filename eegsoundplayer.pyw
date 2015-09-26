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

import fnmatch, random, signal, subprocess, sys, time
import numpy as np

pyqtversion = 5
if pyqtversion == 4:
    from PyQt4 import QtCore, QtGui
    from PyQt4.QtCore import Qt, QEvent, QThread
    from PyQt4.QtGui import QAction, QApplication, QCheckBox, QComboBox, QDesktopServices, QDesktopWidget, QDoubleValidator, QFrame, QFileDialog, QGridLayout, QHBoxLayout, QIcon, QIntValidator, QLabel, QLayout, QLineEdit, QMainWindow, QMessageBox, QProgressBar, QScrollArea, QSizePolicy, QSpacerItem, QSplitter, QPushButton, QVBoxLayout, QWhatsThis, QWidget
    QFileDialog.getOpenFileName = QFileDialog.getOpenFileNameAndFilter
    QFileDialog.getOpenFileNames = QFileDialog.getOpenFileNamesAndFilter
    QFileDialog.getSaveFileName = QFileDialog.getSaveFileNameAndFilter
    Signal = QtCore.pyqtSignal
    Slot = QtCore.pyqtSlot
elif pyqtversion == -4:
    import PySide
    from PySide import QtCore, QtGui
    from PySide.QtCore import Qt, QEvent, QThread, Signal, Slot
    from PySide.QtGui import QAction, QApplication, QCheckBox, QComboBox, QDesktopServices, QDesktopWidget, QDoubleValidator, QFrame, QFileDialog, QGridLayout, QHBoxLayout, QIcon, QIntValidator, QLabel, QLayout, QLineEdit, QMainWindow, QMessageBox, QProgressBar, QScrollArea, QSizePolicy, QSpacerItem, QSplitter, QPushButton, QVBoxLayout, QWhatsThis, QWidget
elif pyqtversion == 5:
    from PyQt5 import QtCore, QtGui
    from PyQt5.QtCore import Qt, QEvent, QThread
    from PyQt5.QtWidgets import QAction, QApplication, QCheckBox, QComboBox, QDesktopWidget, QFrame, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QLayout, QLineEdit, QMainWindow, QMessageBox, QProgressBar, QScrollArea, QSizePolicy, QSpacerItem, QSplitter, QPushButton, QVBoxLayout, QWhatsThis, QWidget
    from PyQt5.QtGui import QDesktopServices, QDoubleValidator, QIcon, QIntValidator
    Signal = QtCore.pyqtSignal
    Slot = QtCore.pyqtSlot
signal.signal(signal.SIGINT, signal.SIG_DFL)

from eegsoundplayer import qrc_resources

class EEGSoundPlayer(QMainWindow):
    def __init__(self, parent=None, prm=None):
        QMainWindow.__init__(self, parent)
        self.cw = QFrame()
        self.gridBox = QGridLayout()
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

        self.vBox = QVBoxLayout()
        self.vBox.addLayout(self.gridBox)
        self.vBox.addWidget(self.gauge)
        self.vBox.addWidget(self.blockGauge)

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

        self.nBlocks = 0
        self.totalCount = 0
        self.runningBlock = False
        self.playing = False
        self.stimListLoaded = False
        self.finishedSession = False
        self.logFileIsOpen = False
        self.show()
        
    def updateGauge(self, val):
        self.gauge.setValue(val)

    def updateStatus(self):
        self.blockGauge.setRange(0, self.nBlocks)
        self.blockGauge.setValue(self.currentBlock-1)
        self.blockGauge.setFormat("Blocks Completed" +  ': ' + str(self.currentBlock-1) + '/' + str(self.nBlocks))
        self.currentBlockLabel.setText("Block Label: " + self.blockLabels[self.currentBlock-1])
        self.currentBlockPositionLabel.setText("Block Position: " + str(self.currentBlock))
        self.storedBlocksLabel.setText("Stored Blocks: " + str(self.nBlocks))
        if self.stimListLoaded == True:
            self.totalCount = len(self.trialList[self.blockLabels.index('B'+str(self.currentBlock))])

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
        self.finishedSession = False
        self.runningBlock = False
        self.playing = False
        self.currentBlock = 1
        self.currentCount = 0
        self.gauge.setValue(0)
        self.updateStatus()
            
    def onClickSoundPlayButton(self):
        if self.stimListLoaded == False:# or self.finishedSession == True:
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
            self.totalCount = len(self.trialList[self.blockLabels.index('B'+str(self.currentBlock))])
            self.updateStatus()
        print(self.blockLabels)
        self.runningBlock = True
        if self.playing == False:
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

    def onClickSoundPauseButton(self):
        self.playThread.terminate()

    def moveToNextBlock(self):
        self.runningBlock = False
        self.playing = False
        self.logFile.flush()
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
            self.logFile.close()
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
                if ln[0:3] == "ISI":# and ln.split(":")[1].strip() == "True":
                    if len(ln.split(":")[1].split("-")) == 1:
                        self.ISITypeChooser.setCurrentIndex(0)
                        ISI = ln.split(":")[1].strip()
                        self.ISIBox.setText(ISI)
                    else:
                        self.ISITypeChooser.setCurrentIndex(1)
                        ISIMin = ln.split(":")[1].split("-")[0].strip()
                        ISIMax = ln.split(":")[1].split("-")[1].strip()
                        self.ISIMinBox.setText(ISIMin)
                        self.ISIMaxBox.setText(ISIMax)
            self.stimListLoaded = True
            self.statusBar().showMessage("Ready")
            self.totalCount = len(self.trialList[0])
            self.updateStatus()

    def onClickSaveLogButton(self):
        ftow = QFileDialog.getSaveFileName(self, self.tr('Choose file to write log'), "", self.tr('All Files (*)'), "", QFileDialog.DontConfirmOverwrite)[0]
        if len(ftow) > 0:
            if fnmatch.fnmatch(ftow, '*.txt') == False:
                ftow = ftow + '.txt'
            self.logFile = open(ftow, 'a')
            self.logFileIsOpen = True

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
         
class threadedPlayer(QThread):
    progress = Signal(int)
    blockCompleted = Signal()
    def __init__(self, parent):
        QThread.__init__(self, parent)
        
    def playThreadedSound(self):
        self.start()
    def run(self):
        while self.parent().currentCount < self.parent().totalCount and self.parent().runningBlock == True:
            print("Playing: " + self.parent().trialList[self.parent().blockLabels.index('B'+str(self.parent().currentBlock))][self.parent().currentCount])
            filePath = self.parent().trialList[self.parent().blockLabels.index('B'+str(self.parent().currentBlock))][self.parent().currentCount]
            subprocess.call('aplay ' + filePath, shell=True)
            if self.parent().ISITypeChooser.currentText() == "Fixed":
                ISI = int(self.parent().ISIBox.text())
            else:
                ISI = random.uniform(int(self.parent().ISIMinBox.text()), int(self.parent().ISIMaxBox.text()))
            time.sleep(ISI/1000)
            self.parent().logFile.write(filePath + ";" + self.parent().blockLabels[self.parent().currentBlock-1] + ";" + self.parent().subjID.text() + "\n")
            
            self.parent().currentCount = self.parent().currentCount + 1
            pcTot = self.parent().currentCount / self.parent().totalCount * 100
            self.progress.emit(int(pcTot))
            if self.parent().currentCount == self.parent().totalCount:
                self.blockCompleted.emit()

def main():
    
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon.fromTheme("media-playback-start", QIcon(":/media-playback-start")))
    ex = EEGSoundPlayer()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main() 