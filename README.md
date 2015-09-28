``eegsoundplayer`` is a small application written to play lists of WAV files for electroencephalography (EEG) experiments. The application is tailored to the setup of our EEG lab. We don't send trigger codes through the parallel port. Instead, we use the first two channels of the soudcard to play sounds, and we use the additional channels to send the trigger codes through a custom-made hardware box. The triggers are embedded in multichannel WAV files. Therefore, all that ``eegsoundplayer`` has to do is play these WAV files. This is a rather simple operation which could be easily accomplished by a command-line script. However, ``eegsoundplayer`` is convenient because a) it has an intuitive graphical user interface, and b) it allows you to pause and resume the playback of the WAV files.

``eegsoundplayer`` uses a commandline utility to play WAV files (``aplay`` on Linux, and ``afplay`` on MAC OS X). ``eegsoundplayer`` has been tested on Linux and should work on MAC OS X too (although this has not been tested). ``eegsoundplayer`` currently doesn't work on Windows.