# coding=utf-8
'''
Created on 2014年10月15日

@author: Peter Hao Zong
'''

import urllib2
from bs4 import BeautifulSoup
import codecs
import re
from macpath import join
import time
from multiprocessing.dummy import Pool as ThreadPool 

print 'begin'
iterdict = {}

def load_Dict(filename):
    Dict_file = open(filename,'rb')
    index = 0
    dictonary = {}
    for line in Dict_file.readlines():
        dictonary[line.strip()] = index
        index += 1
    return dictonary

def webclawl(fword):
    urlist = []
    urlist.append('http://dict.youdao.com/search?q=lj:%s&ljtype=blng&ljblngcont=0&le=eng&keyfrom=dict.main.moreblng' %fword)
    urlist.append('http://dict.youdao.com/search?q=lj%3A' + fword + '&ljtype=blng&ljblngcont=1&keyfrom=dict.sentence.details.kouyu')
    urlist.append('http://dict.youdao.com/search?q=lj%3A' + fword + '&ljtype=blng&ljblngcont=2&keyfrom=dict.sentence.details.shumian')
    urlist.append('http://dict.youdao.com/search?q=lj%3A' + fword + '&ljtype=blng&ljblngcont=1&keyfrom=dict.sentence.details.kouyu')
    COUNT = 1
    for url in urlist:
        print url
        try:
            pageinfo = urllib2.urlopen(url,timeout=10)
            page = pageinfo.read()
#             pagesave = open('pagesave/' + fword +str(COUNT) + '.html','wb')
#             pagesave.write(page)
            COUNT += 1
        #     pagefile = open('example.txt','rb')
        #     plaininfo = pagefile.read()
            soup = BeautifulSoup(page)
            sentencelistinfo = soup.find('div',id='examples_sentences')
            sentencelist = sentencelistinfo.find_all('li')
            count = 1
            # print sentencelist
            for sentence in sentencelist:
                sentenceinfo = sentence.find_all('p')
                src = sentenceinfo[0]
                srclist = src.find_all('span')
                srcstring = ''
                alignlist = []
                srcdic = {}
                srccount = 0
                tgtcount = 0
                tgtdic = {}
                srcpdic = {}
                tgtpdic = {}
                for word in srclist:
                    pattern = r'onmouseover=\"hlgt\(\'(.*?)\'\)\"'
                    p = re.compile(pattern)
                    idpattern = r'id=\"(.*?)\"'
                    idp = re.compile(idpattern)
                    idinfo = idp.findall(str(word))
                    phrase = word.get_text()
                    if idinfo:
                        srcpdic[idinfo[0]] = phrase
            #             print idinfo,phrase
                    aligninforaw = p.findall(str(word))
                    for aligninfo in aligninforaw:
                        if aligninfo:
                            align = aligninfo.split(',')
            #                 print align
            #                 print align,len(align),align[0],align[1]
                            srclist = align[0].split('#')
                            tgtlist = align[1].split('#')
                            srcstring = ''
                            tgtstring = ''
                            for srcs in srclist:
                                if srcs:
                                    srcstring += srcs+','
                            for tgts in tgtlist:
                                if tgts:
                                    tgtstring += tgts+','
            #                 print srcstring.strip(','),tgtstring.strip(',')
                            alignstring = srcstring.strip(',') + ':' +tgtstring.strip(',')
                            alignlist.append(alignstring)
                    srcstring += word.get_text() + '\t'
            #     print srcstring.rstrip('\t')
                tgt = sentenceinfo[1]
                srcplistraw = src.find_all('span')
                srcplist = []
                for srcp in srcplistraw:
                    if srcp.get_text().strip(' '):
                        srcplist.append(srcp.get_text())
                        srcdic[srcp.get_text().strip(' ')] = srccount
                        srccount += 1
                tgtplistraw = tgt.find_all('span')
                for word in tgtplistraw:
                    idpattern = r'id=\"(.*?)\"'
                    idp = re.compile(idpattern)
                    idinfo = idp.findall(str(word))
                    phrase = word.get_text()
                    if idinfo:
                        tgtpdic[idinfo[0]] = phrase
                tgtplist = []
                for tgtp in tgtplistraw:
                    if tgtp.get_text().strip(' '):
                        tgtplist.append(tgtp.get_text())
                        tgtdic[tgtp.get_text().strip(' ')] = tgtcount
                        tgtcount += 1
                turealignlist = []
                for alignsubinfo in alignlist:
                    alignsplit = alignsubinfo.split(':')
                    alignstr = ''
                    srcno = ''
                    for srcphrase in alignsplit[0].split(','):
                        srcno = srcdic[srcpdic[srcphrase]]
            #             alignstr += str(srcno) + ','
            #         alignstr = alignstr.rstrip(',')
            #         alignstr += '-'
                    for tgtphrase in alignsplit[1].split(','):
                        tgtno = tgtdic[tgtpdic[tgtphrase]]
                        alignstr += str(srcno) + '-' + str(tgtno) + ' '
                    turealignlist.append(alignstr.rstrip(' '))
    #             print '\t'.join(srcplist)
    #             print '\t'.join(tgtplist)
                srcsentence = '\t'.join(srcplist)
                tgtsentence = '\t'.join(tgtplist)
                savefile.write(srcsentence+'\n')
                savefile.write(tgtsentence+'\n')
                outstr = str(len(srcplist)) + '-' + str(len(tgtplist)) + ' ||| ' +' '.join(turealignlist)
                savefile.write(outstr+'\n')
                return (srcsentence,tgtsentence,str)
    #             print outstr
        except:
            pass
            
#     for key,val in srcdic.items():
#         print key,val
#     print ' '.join(alignlist)
#     print count 
#     count += 1
#     print src,'\n',tgt

#     print src, tgt
# print sentencelistinfo

dictfile = '21dict.txt'
mydict = load_Dict(dictfile)
savefile = codecs.open('youdao_10.txt','a+','utf8')
INDEX = 1
itemlist = []
for item in mydict.keys():
    if INDEX > 1:
        print time.ctime()
        itemlist.append(item)
    if len(itemlist) == 12:
        pool = ThreadPool(12)
        result = pool.map(webclawl, itemlist)
        pool.close()
        pool.join()
        itemlist = []
    INDEX += 1
    
