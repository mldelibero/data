#!/usr/bin/env python

import re
import os
from xlrd import open_workbook
from xlwt import Workbook
from tempfile import TemporaryFile

def toXls(data,filePath):
    '''Save the data in an excel file of the same name as the original data file'''
    #Check to see if the filepath.xls already exists
    path = re.findall(r'(.+)\.TXT',filePath)[0]
    
    newPath = "%s.xls" % (path)
    
    cnt = 0
    while (os.path.exists(newPath)):
        newPath = "%s-%i.xls" % (path,cnt)
        cnt+=1

    print "Saving data to: ",newPath
    #Save data in file
    params = re.findall(r'(\w+)',data['settings'][1][1])
    wb = Workbook()
    wsA = wb.add_sheet(params[0])
    wsB = wb.add_sheet(params[1])
    wsSet = wb.add_sheet('settings')

    #Settings
    col= 0
    for set in data['settings']:
        wsSet.write(col,0,set[0])
        wsSet.write(col,1,set[1])
        col+=1

    #TraceA
    col=0
    for head in data['headA']:
        wsA.write(0,col,head)
        col+=1
    row = 1
    for pts in data['dataA']:
        col = 0
        for pt in pts:
            wsA.write(row,col,pt)
            col+=1
        row+=1
    
    #TraceB
    col=0
    for head in data['headB']:
        wsB.write(0,col,head)
        col+=1
    row = 1
    for pts in data['dataB']:
        col = 0
        for pt in pts:
            wsB.write(row,col,pt)
            col+=1
        row+=1

    wb.save(newPath)
    wb.save(TemporaryFile())

