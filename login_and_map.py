#!/usr/bin/env python

import os, shutil, pwd, grp, subprocess

empty = True
moved = False
curuser = pwd.getpwuid(os.stat('/dev/console').st_uid)[0]
curgroup = grp.getgrgid(os.stat('/dev/console').st_gid)[0]
homedir = '/Users/' + curuser
folders = ['/Desktop']


if 'AD' in curgroup:

    print "AD Mapping Script: User is network defined."

    for folder in folders:
        curpath = homedir + folder

        if not os.path.islink(curpath):

            for f in os.listdir(curpath):
                fp = os.path.join(curpath, f)
                if os.path.isfile(fp) and not f.startswith('.'):
                    empty = False
                if os.path.isdir(fp):
                    empty = False

            if empty:
                print "current path:" + curpath
                print "AD Mapping Script: Directory is empty - deleting and redirecting."
                shutil.rmtree(curpath)
                os.symlink("/Volumes/" + os.getlogin() + "$" + folder, curpath)
                moved = True
            else:
                print "current path:" + curpath
                print "AD Mapping Script: Directory is not empty - copying to /Users/Shared/" + os.getlogin() + folder + " and redirecting userdir to network home"
                shutil.move(curpath, "/Users/Shared/" + os.getlogin() + folder)
                os.symlink("/Volumes/" + os.getlogin() + "$" + folder, curpath)
                moved = True
                
        else:
            print "AD Mapping Script: " + curpath + " is already linked"

    if moved:
        subprocess.call(['/usr/bin/killall', 'Finder'])

else:
    print "AD Mapping Script: User " + os.getlogin() + " is local - not redirecting folders."

subprocess.call(['/usr/bin/rm', '/private/tmp/edu.syr.cas.adusermapping.runatload'])
