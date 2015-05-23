# coding=utf-8
'''
Created on 2014年11月26日

@author: Peter Hao Zong
'''
import codecs 

def file_split(filename,numberofline):
    sourcefile = codecs.open(filename,'rb','utf8')
    filecount = 1
    line = sourcefile.readline()
    linecount = 1
    outfile = codecs.open(filename+str(filecount),'wb','utf8')
    while line:
        linecount += 1
        if linecount == numberofline:
            filecount += 1
            outfile = codecs.open(filename+str(filecount),'wb','utf8')
            linecount = 1
        outfile.write(line)
        line = sourcefile.readline()
file_split('youdao_4.txt', 1000000)