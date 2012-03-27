#!/usr/bin/env python
import re
from math import atan2,pi

calcOpts = {'phase_zy':1,'b':2,'c':3,'d':4,'q':6,'e':5}
paramOpts = {'IMPEDANCE':['phase_zy','c','q','e']}


def phase_zy(dat):
    cnt = 0
    for d in dat:
        dat[cnt] = d + tuple([atan2(float(d[2]),float(d[1]))*180/pi])
        cnt+=1

    return dat

def calc(data,choice):
    '''Take the data and add a calculation column'''
    'choice = [trace,caluculation]'
    
    if choice[1] == 'phase_zy':
        data[choice[0]] = phase_zy(data[choice[0]])
        head = re.sub(r'data(A|B)',r'head\1',choice[0])
        data[head] += tuple(["Calc Phase (deg)"])

    else:
        print "error -- invalid choice"
    return data

def getCalc(data):
    '''Ask user if he wants to calculate anything and then add that to the data and return the data'''
    params = re.findall(r'(\w+)',data['settings'][1][1])
    for param in params:
        calcChoices = []
        cnt = 1
        for opt in calcOpts:
            try:
                for op in paramOpts[param]:
                    if op == opt:
                        if cnt == 1:
                            print "\nFor %s, do you want to calc?" % param
                            print "--Put in a csv list"
                            print "[0] Nothing"
                        print "[%i] %s" % (cnt,opt)
                        cnt+=1
                        calcChoices.append(opt)
            except KeyError:
                a = 1

    
        if cnt > 1:
            ans = int(raw_input(''))
            try:
                for an in ans:
                    print an
                    if an == 0:
                        b = 1 #do nothing
                    else:
                        if param == params[0]:
                            trace = 'dataA'
                        else:
                            trace = 'dataB'
                        choice = [trace,calcChoices[int(an)-1]]
                        data = calc(data,choice)
            except TypeError:
                print ans
                if ans == 0:
                    a = 1
                else:
                    if param == params[0]:
                        trace = 'dataA'
                    else:
                        trace = 'dataB'
                    print calcChoices
                    choice = [trace,calcChoices[int(ans)-1]]
                    data = calc(data,choice)

    return data
