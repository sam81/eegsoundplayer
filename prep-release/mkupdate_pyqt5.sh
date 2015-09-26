

pyrcc5 -o ../eegsoundplayer/qrc_resources.py ../resources.qrc
pylupdate5 -verbose eegsoundplayer.pro
lrelease -verbose eegsoundplayer.pro

mv *.qm ../translations/
