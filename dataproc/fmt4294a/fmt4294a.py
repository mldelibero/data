#!/usr/bin/env python
import os
import sys
import re

from getFile import getFile
from getData import getData
from toXls import toXls

#    file = open(filePath,'r')

def display():
    '''Display data in graph

        Not currently implemented
    '''
    a = 1
if __name__=='__main__':
    path = getFile()
    data = getData(path)
    toXls(data,path)
    display()
