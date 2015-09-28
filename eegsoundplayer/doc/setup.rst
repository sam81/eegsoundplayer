

*****
Setup
*****

.. _sec-stim_list_files:

Stimulus List Files
===================

The stimulus list files are simple text files listing the WAV files to be played during an experimental session. An experimental session is divided into one or more "blocks", each block consists of one or more "trials". In a stimulus list file the beginning of a block is marked by a line with a sequence of 10 ``+`` signs, and the end of a block by a line with a sequence of 10 ``-`` signs. Each line between the beginning and the end of a block contains the file path to a WAV file to be played in that block of trials. For example, the following stimulus list contains two blocks with three trials on each block:

::

   ++++++++++
   /home/sam/stimuli/snd_a_1.wav
   /home/sam/stimuli/snd_a_2.wav
   /home/sam/stimuli/snd_a_3.wav
   ----------
   ++++++++++
   /home/sam/stimuli/snd_b_1.wav
   /home/sam/stimuli/snd_b_2.wav
   /home/sam/stimuli/snd_b_3.wav
   ----------

Optionally, a stimulus list file can contain directives specifying whether the blocks should be randomized, and whether the trials within blocks should be randomized. If you want the blocks to be randomized, just put a line on top of the file that says ``Shuffle Blocks: True``. If you want the trials within blocks to be randomized, just put a line on top of the file that says ``Shuffle Trials: True``. If you replace ``True`` with ``False``, or omit the line, the blocks/trials won't be randomized. An example stimulus list with both block, and trial randomization is given below:

::

   Shuffle Blocks: True
   Shuffle Trials: True
   ++++++++++
   /home/sam/stimuli/snd_a_1.wav
   /home/sam/stimuli/snd_a_2.wav
   /home/sam/stimuli/snd_a_3.wav
   ----------
   ++++++++++
   /home/sam/stimuli/snd_b_1.wav
   /home/sam/stimuli/snd_b_2.wav
   /home/sam/stimuli/snd_b_3.wav
   ----------

Please, note that these directives will only put a check on the "Shuffle Blocks" and "Shuffle Trials" checkboxes in the ``eegsoundplayer`` window when the stimulus list is loaded. If the checkboxes are subsequently unchecked by the user no randomization will occur.
   
Finally, the stimulus list file can specify the ISI to be used. If you for example want a fixed 500-ms ISI just put a line with ``ISI: 500`` on top of the stimulus list file. If you want a random uniform ISI between for example 200 and 500 ms, just put a line with ``ISI: 200-500`` on top of the stimulus list file. An example is given below:

::

   ISI: 200-500
   Shuffle Blocks: True
   Shuffle Trials: False
   ++++++++++
   /home/sam/stimuli/snd_a_1.wav
   /home/sam/stimuli/snd_a_2.wav
   /home/sam/stimuli/snd_a_3.wav
   ----------
   ++++++++++
   /home/sam/stimuli/snd_b_1.wav
   /home/sam/stimuli/snd_b_2.wav
   /home/sam/stimuli/snd_b_3.wav
   ----------

.. _sec-log_file:

Log File
========

The log file records the sequence of stimuli that was played. This is useful if the blocks and/or trials are randomized and the user wants to know the exact presentation sequence of the stimuli. The log file also records the block label, the participant ID (if provided), a date stamp, and a time stamp. If the user has not selected a log file prior to the beginning of a session s/he will be prompted to do so when the session begins.

Besides the log file, another file will be written by ``eegsoundplayer``. This file has the same root name as the chosen log file but has an additional ``_stderr`` suffix. This file records the standard error (stderr) output of the command that was invoked to play the file (``aplay`` on Linux, ``afplay`` on MAC OS X). This is useful to check that playback of the files went smoothly without errors or glitches. ``aplay`` for example will log buffer underruns as well as failures to find a file to stderr.

.. _sec-randomization:

Randomization
=============

By default the blocks and the trials within blocks are presented in the same order in which they are listed in the stimulus list file. When a stimulus list file is loaded, the blocks are also labelled sequentially as "B1", "B2", etc... according to the order in which they appear in the stimulus list file. If you want to present the blocks in a random order, the ``Shuffle Blocks`` checkbox needs to be checked before the start of a session. Similarly, if you want the trials within blocks to be presented in a random order, the ``Shuffle Trials`` checkbox needs to be checked before the start of a session. The randomization occurs when the user hits the ``Play`` button and the current block position is 1. No randomization will occur if the user moves to another block position before hitting the ``Play`` button because in that case the session is considered as already started (even if the user simply navigated between blocks with the ``Next``/``Previous`` buttons). When the block randomization occurs the block labels remain the same, but the block positions, which mark the position at which each block will be presented during a session are shuffled. The ``Reset`` button removes the randomization (as well as resetting the current session if a session has already started).

Occasionally you may want to repeat a block of trials at the end of a session because the EEG was noisy during the first presentation of that block. In this case, you need to note the block label (e.g. B3), and navigate with the ``Next`` or ``Previous`` button to the block you want to repeat. Make sure that the ``Shuffle Blocks`` checkbox is not checked because otherwise, if the block that you want to repeat happens to be in position 1, the blocks will be automatically randomized and you may not start the block you intended to repeat.
