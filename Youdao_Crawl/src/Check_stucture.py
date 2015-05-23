# coding=utf-8
'''
Created on 2014年11月14日

@author: Peter Hao Zong
'''
import codecs
inputfile = codecs.open('youdao_5.txt','rb','utf8')
line = inputfile.readline()
index = 1
linelist = []
# while line:
#     if index > 1:
#         if index % 3 == 0:
#             temp = line.split('|||')
#             if len(temp)!=2:
#                 print index
#                 break
#     index += 1
#     line = inputfile.readline()
linecount = 1
outputfile = codecs.open('youdao_5.clean.txt','wb','utf8')
while line:
    linelist.append(line)
    temp = line.split('|||')
    if len(temp) == 2:
        if index != 3:
            print index,linecount,len(linelist)
        else:
            for linestr in linelist:
                outputfile.write(linestr)
        index = 0
        linelist = []
    index += 1
    linecount += 1
    line = inputfile.readline()