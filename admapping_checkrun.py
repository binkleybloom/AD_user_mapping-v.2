#!/usr/bin/env python

import os, shutil, pwd, grp, subprocess

curgroup = grp.getgrgid(os.stat('/dev/console').st_gid)[0]

if 'AD' in curgroup:
    subprocess.call(['/usr/bin/touch', '/private/tmp/edu.syr.cas.adusermapping.runatload'])
