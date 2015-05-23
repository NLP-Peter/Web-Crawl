# coding=utf-8
'''
Created on 2014年11月13日

@author: Peter Hao Zong
'''

sourcefile = open('21','rb')
outputfile = open('21dict.txt','wb')
for line in sourcefile.readlines():
    temp = line.split('\t')
    outputfile.write(temp[0]+ '\n')