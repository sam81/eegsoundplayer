.. _sec-user_interface:

**************
User Interface
**************

Main Window
============

Below is a description of each element present in the graphical user interface.

-  **Play** The ``Play`` button starts playing the WAV files in a loaded stimulus file list. While stimulus playback is ongoing the play button turns into a ``Pause`` button that can be used to suspend stimulus playback temporarily.

- **Load Stim. List** The ``Load Stim. List`` button can be used to load file containing a list of stimuli to be played in an experimental session. The format of the stimulus list file is described in section :ref:`sec-stim_list_files`.

- **Choose Log File** The ``Choose Log File`` button can be used to select the log file in which the sequence of stimuli played is logged along with the block label, the participant ID (if provided), a date stamp, and a time stamp. If an existing file is selected, this file will not be overwritten, instead, the logs will be appended at the end of the selected file.

- **Reset** The ``Reset`` button resets a session. This includes moving to the first block, and resetting the count of stimuli played in the soundlist.

- **Sound Check** The ``Sound Check`` button allows you to play a short melody in a loop to check that sound output is working. While the melody is playing the ``Sound Check`` button turns into a ``Stop Sound Check`` button that can be used to stop the sound check.

- **Participant ID Text Field** Here you can enter an identifier for the participant. This identifier will be stored in the log file.

- **ISI Type** Choose whether you want a fixed inter-stimulus interval (ISI), or an variable ISI randomly drawn from a uniform distribution.

- **ISI (ms)** Set the ISI. This text field appears only when ``ISI Type`` is ``Fixed``

- **Min. ISI (ms)** Set the minimum ISI. This text field appears only when ``ISI Type`` is ``Random Uniform``

- **Max. ISI (ms)** Set the maximum ISI. This text field appears only when ``ISI Type`` is ``Random Uniform``

- **Previous** Move to the previous block.

- **Next** Move to the next block.

- **Block Label** This is a label identifying the current block of trials. Blocks are labelled according to the order in which they are listed in the stimulus list file as "B1", "B2", "B3", etc...

- **Stored Blocks** The number of blocks stored in the current stimulus file.

- **Block Position** The position at which the current block will be presented. See :ref:`sec-randomization` for further info.

- **Shuffle Blocks** If this checkbox is checked, the blocks will be randomized before the start of a session. The randomization occurs when the user hits the ``Play`` button and the current block position is 1. No randomization will occur if the user moves to another block position before hitting the ``Play`` button.

- **Shuffle Trials** If this checkbox is checked, the trials will be randomized before the start of a session. The randomization occurs when the user hits the ``Play`` button and the current block position is 1. No randomization will occur if the user moves to another block position before hitting the ``Play`` button.

File Menu
=========

- **Open Stim. List** Open the stimulus list file for inspection. A stimulus list needs to be loaded in order to open it.

- **Open Log File** Open the log file for inspection (see :ref:`sec-log_file`. A log file needs to be already selected in order to open it.

- **Open stderr File** Open the stderr file for inspection (see :ref:`sec-log_file`. An stderr file needs to be already selected in order to open it.
