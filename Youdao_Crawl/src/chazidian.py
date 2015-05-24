# coding=utf-8
'''
Created on 2015年5月22日

@author: Peter Hao Zong
'''
from bs4 import BeautifulSoup
import urllib2
import time
from utils import load_Dict
import codecs
from multiprocessing.dummy import Pool as ThreadPool 


def crawl_chazidian(word):
    try:
        url = 'http://www.chazidian.com/dict/' + word + '/'
        html = urllib2.urlopen(url,timeout=10).read()
        soup = BeautifulSoup(html)
        container = soup.find_all('div', class_ = 'dict_sentence')
        pairlist = container[0].find_all('p')
        cnt = 1 
        cn = []
        en = []
        example_sentence = []
        for pair in pairlist:
            if cnt %2 == 0:
                cn.append(pair.get_text())
            else:
                en.append(pair.get_text())
            cnt += 1
        for i in range(len(cn)):
            example_sentence.append([en[i],cn[i]])   
        return example_sentence
    except:
        pass  
    
dictfile = 'dict.en'
mydict = load_Dict(dictfile)
savefile = codecs.open('chazidian.txt','a+','utf8')
INDEX = 1
itemlist = []
targetindex = 9999999
for item in mydict.keys():
    if INDEX > 1:
        print time.ctime(),INDEX
        itemlist.append(item)
    if len(itemlist) == 20:
        pool = ThreadPool(8)
        result = pool.map(crawl_chazidian, itemlist)
        pool.close()
        pool.join()
        for elelist in result: 
            if elelist != None:
                for ele in elelist:
                    savefile.write(ele[0] + '\n')
                    savefile.write(ele[1] + '\n')
        itemlist = []
    INDEX += 1
