# coding=utf-8
'''
Created on 2014年11月27日

@author: Peter Hao Zong
'''
# this is a program to remove the duplicated sentence pairs, the data format is following  src,tgt,target.
import codecs

def remove_duplicate(inputfilename,outputfilename):
    source = codecs.open(inputfilename,'rb','utf8')
    out = codecs.open(outputfilename, 'wb', 'utf8')
    reference_dic = {}
    line = source.readline()
    while line:
        if reference_dic.has_key(line):
            line = source.readline()
            line = source.readline()
        else:
            reference_dic[line] = 1
            out.write(line)
            out.write(source.readline())
            out.write(source.readline())
        line = source.readline()
remove_duplicate('youdao_5.clean.txt', 'youdao_clean.txt')