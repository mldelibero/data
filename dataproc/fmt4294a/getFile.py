#!/usr/bin/env python
import os
import re

def getFile():
    '''Get file from user and make sure that it exists.
        Return the file and path as a string
    '''
    path = os.path.abspath('./')
    tempNames = os.listdir(path)
    
    fnames = []
    for name in tempNames:
        mat = re.findall(r'\w+\.TXT',name)
        if mat:
            fnames.append(name)
        
    print "You are here: ",path
    print "Which file do you want to process?"

    if len(fnames) == 0:
        print "Error: Expected to find a .TXT file in dir" 
        sys.exit(0)

    cnt = 0
    for file in fnames:
        print "[%s]  %s" % (cnt,file)
        cnt+=1
    
    ans = int(raw_input(''))
    fname = fnames[ans]
    f_full = "%s/%s" % (path,fname)
    
    return f_full
