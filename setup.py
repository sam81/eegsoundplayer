#! /usr/bin/env python
from distutils.core import setup
import glob
setup(
    name="eegsoundplayer",
    version="0.0.10",
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
    packages=["eegsoundplayer"],
    scripts = ["eegsoundplayer.pyw"],
    package_dir={"eegsoundplayer": "eegsoundplayer"},
    package_data={'eegsoundplayer': ["qrc_resources.py",
                                     "doc/_build/latex/*.pdf",
                                     "doc/_build/html/*.*",
                                     "doc/_build/html/_images/*",
                                     "doc/_build/html/_modules/*",
                                     "doc/_build/html/_sources/*.*",
                                     "doc/_build/html/_sources/_templates/autosummary/*.*",
                                     "doc/_build/html/_sources/_themes/*.*",
                                     "doc/_build/html/_static/*.*",
                                     "doc/_build/html/_static/css/*.*",
                                     "doc/_build/html/_static/font/*.*",
                                     "doc/_build/html/_static/js/*.*",
                                     "doc/_build/html/_templates/autosummary/*.*",
                                     "doc/_build/html/_themes/*.*"],},

    
    data_files = [('share/applications', ['eegsoundplayer.desktop']),
                  ('share/icons', ['icons/eegsoundplayer.svg']),
                  ]

    )


