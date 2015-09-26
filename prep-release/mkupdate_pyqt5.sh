

pyrcc5 -o ../EEGSoundPlayer/qrc_resources.py ../resources.qrc
pylupdate5 -verbose EEGSoundPlayer.pro
lrelease -verbose EEGSoundPlayer.pro

mv *.qm ../translations/
