#! /usr/bin/env python
from distutils.core import setup
import glob
setup(
    name="EEGSoundPlayer",
    version="0.0.2",
    url="",
    author="Samuele Carcagno",
    author_email="sam.carcagno@google.com;",
    description="Python application for playing sound in an EEG experiment",
    long_description=\
    """
    Python application for playing sound in an EEG experiment
    """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
        ],
    license="GPL v3",
    requires=['PyQt (>=5.3.2)', 'numpy (>=1.6.1)', 'scipy (>=0.10.1)'],
    packages=["EEGSoundPlayer"],
    scripts = ["EEGSoundPlayer.pyw"],
    package_dir={"EEGSoundPlayer": "EEGSoundPlayer"},
    package_data={'EEGSoundPlayer': ["qrc_resources.py"]}#,

    
    # data_files = [('share/applications', ['pychoacoustics.desktop']),
    #               ('share/icons', ['icons/Machovka_Headphones.svg']),
    #               ]

    )


