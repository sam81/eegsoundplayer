#! /usr/bin/env python
# -*- coding: utf-8 -*-

import getopt, datetime, os, subprocess, sys
os.chdir('../')

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "m:", ["message="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-m", "--message"):
            message = arg
    major_v = 0
    minor_v = 0

    #read minor minor release number
    f = open('prep-release/minor_minor_number.txt', 'r')
    ln = f.readlines()
    f.close()
    minor_minor_v = int(ln[0].strip()) + 1
    #write incremented minor minor release number
    f = open('prep-release/minor_minor_number.txt', 'w')
    f.write(str(minor_minor_v))
    f.close()
    builddate = datetime.datetime.now().strftime("%d-%b-%Y %H:%M")
    #set git tag
    gittag = str(major_v) + '.' + str(minor_v) + '.' + str(minor_minor_v)
    
    f = open('setup.py', 'r')
    ln = f.readlines()
    f.close()
    for i in range(len(ln)):
        if ln[i].strip().split('=')[0].strip() == "version":
            ln[i] = '    version="' + gittag +'",\n'

    f = open('setup.py', 'w')
    f.writelines(ln)
    f.close()

    # f = open('setup-pyside.py', 'r')
    # ln = f.readlines()
    # f.close()
    # for i in range(len(ln)):
    #     if ln[i].strip().split('=')[0].strip() == "version":
    #         ln[i] = '    version="' + gittag +'",\n'

    # f = open('setup-pyside.py', 'w')
    # f.writelines(ln)
    # f.close()


    # f = open('setup-pyqt4.py', 'r')
    # ln = f.readlines()
    # f.close()
    # for i in range(len(ln)):
    #     if ln[i].strip().split('=')[0].strip() == "version":
    #         ln[i] = '    version="' + gittag +'",\n'

    # f = open('setup-pyqt4.py', 'w')
    # f.writelines(ln)
    # f.close()
    

    f = open('eegsoundplayer/_version_info.py', 'r')
    ln = f.readlines()
    f.close()
    for i in range(len(ln)):
        if ln[i].strip().split('=')[0].strip() == "eegsoundplayer_version":
            ln[i] = 'eegsoundplayer_version = "' + gittag +'"\n'
        if ln[i].strip().split('=')[0].strip() == "eegsoundplayer_builddate":
            ln[i] = 'eegsoundplayer_builddate = "' + builddate +'"\n'

    f = open('eegsoundplayer/_version_info.py', 'w')
    f.writelines(ln)
    f.close()


    f = open('eegsoundplayer/doc/conf.py', 'r')
    ln = f.readlines()
    f.close()
    for i in range(len(ln)):
        if ln[i].strip().split('=')[0].strip() == "version":
            ln[i] = 'version = "' + gittag +'"\n'
        if ln[i].strip().split('=')[0].strip() == "release":
            ln[i] = 'release = "' + gittag + '"\n'

    f = open('eegsoundplayer/doc/conf.py', 'w')
    f.writelines(ln)
    f.close()

    f = open('eegsoundplayer.desktop', 'r')
    ln = f.readlines()
    f.close()
    for i in range(len(ln)):
        if ln[i].strip().split('=')[0].strip() == "Version":
            ln[i] = 'Version = ' + gittag +'\n'

    f = open('eegsoundplayer.desktop', 'w')
    f.writelines(ln)
    f.close()

 
    subprocess.call('git commit -a -m"' + message+'"', shell=True)
    #tag the commit so that it can be easily retrieved
    subprocess.call('git tag -a "' + gittag +'"' + ' -m "' + gittag +'"', shell=True)
    
if __name__ == "__main__":
    main(sys.argv[1:])
