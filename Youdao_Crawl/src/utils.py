# coding=utf-8
'''
Created on 2015年5月22日

@author: Peter Hao Zong
'''

def load_Dict(filename):
    Dict_file = open(filename,'rb')
    index = 0
    dictonary = {}
    for line in Dict_file.readlines():
        dictonary[line.strip()] = index
        index += 1
    return dictonary