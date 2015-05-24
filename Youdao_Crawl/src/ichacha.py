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

url = 'http://www.ichacha.net/search.aspx?q=peter&p='

def crawl_page(url):
    try:
        html = urllib2.urlopen(url, timeout=10)
        soup = BeautifulSoup(html)
        container = soup.find_all('div', id = 'sent_dt1')
        example_sentence = []
        zh = []
        en = []
        sentencesoup = container[0].find_all('td')
        cnt = 1
        print len(sentencesoup)
        for sentence in sentencesoup:
            tt=1
            if cnt % 3 == 0:
                for ele in str(sentence).split('<br/>'):
                    if tt == 1:
                        en.append(BeautifulSoup(ele).get_text())
                    elif tt == 2:
                        zh.append(ele)
                    tt +=1
            cnt += 1
        for i in range(len(zh)):
            example_sentence.append([en[i],zh[i]])
        return example_sentence
    except:
        print 'Extract page: %s\t failed' %url

def crawl_ichacha(word):
    try:
        url = 'http://www.ichacha.net/search.aspx?q=%s&p=' %word
        html = urllib2.urlopen(url, timeout=10)
        soup = BeautifulSoup(html)
        pagesoup = soup.find_all('a', style = 'text-decoration:underline;color:green')
        pagecount = eval(pagesoup[-1].get_text())
        example_sentence = []
        for i in range(1,pagecount+1):
            suburl = url + str(i)
            example_sentence.extend(crawl_page(suburl))
        return example_sentence
    except:
        print 'Extract page: %s\t failed' %url

dictfile = 'dict.en'
mydict = load_Dict(dictfile)
savefile = open('ichacha.txt','a+')
INDEX = 1
itemlist = []
targetindex = 9999999
for item in mydict.keys():
    if INDEX > 1:
        print time.ctime(),INDEX
        itemlist.append(item)
    if len(itemlist) == 20:
        pool = ThreadPool(8)
        result = pool.map(crawl_ichacha, itemlist)
        pool.close()
        pool.join()
        for elelist in result: 
            if elelist != None:
                for ele in elelist:
                    savefile.write(ele[0].encode('utf8') + '\n')
                    savefile.write(ele[1].decode('utf8').encode('utf8')+ '\n')
        itemlist = []
    INDEX += 1
        