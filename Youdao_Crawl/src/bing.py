# coding=utf-8
'''
Created on 2015年5月24日

@author: Peter Hao Zong
'''
from bs4 import BeautifulSoup
import urllib2
import time
from utils import load_Dict
import codecs
from multiprocessing.dummy import Pool as ThreadPool 


def crawl_bing(word):
    url = 'http://cn.bing.com/dict/search?q=' + word
    try:
        html = urllib2.urlopen(url,timeout=10).read()
        soup = BeautifulSoup(html)
        container = soup.find_all('div', id = 'sentenceSeg')
        example_sentence = []
        sentencelist = container[0].find_all('div', class_ = 'se_li')
        for sentence in sentencelist:
            en = sentence.find_all('div', class_ = 'sen_en')[0].get_text()
            zh = sentence.find_all('div', class_ = 'sen_cn')[0].get_text()
            example_sentence.append([en,zh])
        return example_sentence
    except:
        print 'Extract page: %s\t failed' %url
        
dictfile = 'dicttest.txt'
mydict = load_Dict(dictfile)
savefile = codecs.open('bing.txt','a+','utf8')
INDEX = 1
itemlist = []
targetindex = 9999999
for item in mydict.keys():
    if INDEX > 1:
        print time.ctime(),INDEX
        itemlist.append(item)
    if len(itemlist) == 20:
        pool = ThreadPool(8)
        result = pool.map(crawl_bing, itemlist)
        pool.close()
        pool.join()
        for elelist in result: 
            if elelist != None:
                for ele in elelist:
                    savefile.write(ele[0] + '\n')
                    savefile.write(ele[1] + '\n')
        itemlist = []
    INDEX += 1    