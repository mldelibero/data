#!/usr/bin/env python
import os
import sys
import re
from xlrd import open_workbook
from xlwt import Workbook
from tempfile import TemporaryFile

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

#    file = open(filePath,'r')
def getData(filePath):
    '''Extract data from file and return list of formatted data'''
    class stateCl:
       def __init__(self):
           self.config = 1
           self.traceA = 2
           self.traceB = 3
    
    stateI = stateCl()
    state = stateI.config

    data = '(\-{0,1}\d+\.\d+e[\+\-]\d{2})'

    reg_colSep = re.compile(r'"(.+):( +)(.+)"')
    reg_traceA = re.compile(r'TRACE')
    reg_traceB = re.compile(r'^"TRACE: B"')
    reg_data = re.compile(r'^%s\t%s\t%s' % (data,data,data))
    reg_colHead = re.compile(r'^"(Frequency)"\t"(.+)"\t"(.+)"')

    file = open(filePath,'r')
    
    settings = []
    dataA = []
    dataB = []
    headA = []
    headB = []

    for line in file:
        if (state == stateI.config):
            mat = reg_traceA.findall(line)
            if mat:
                if mat:
                    state = stateI.traceA
            else:
                mat2 = reg_colSep.findall(line)
                if mat2:
                    settings.append([mat2[0][0],mat2[0][2]])
        elif (state == stateI.traceA):
            mat = reg_data.findall(line)
            if mat:
                dataA.append(mat[0])
            else:
                mat2 = reg_traceB.findall(line)
                mat3 = reg_colHead.findall(line)
                if mat2:
                    state = stateI.traceB
                if mat3:
                    headA = mat3[0]

        elif (state == stateI.traceB):
            mat = reg_data.findall(line)
            if mat:
                dataB.append(mat[0])
            else:
                mat2 = reg_colHead.findall(line)
                if mat2:
                    headB = mat2[0]
        else:
            print "error in getData() -- Improper state"

    file.close()

    return {'settings':settings,'dataA':dataA,'dataB':dataB,'headA':headA,'headB':headB}

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

def display():
    '''Display data in graph'''
    a = 1
if __name__=='__main__':
    path = getFile()
    data = getData(path)
    toXls(data,path)
    display()
