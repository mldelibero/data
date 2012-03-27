#!/usr/bin/env python

import re
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
