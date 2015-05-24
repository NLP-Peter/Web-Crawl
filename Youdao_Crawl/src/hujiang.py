# coding=utf-8
'''
Created on 2015年5月23日

@author: Peter Hao Zong
'''
from bs4 import BeautifulSoup
import urllib2
import time
from utils import load_Dict
import codecs
from multiprocessing.dummy import Pool as ThreadPool 

url = 'http://dict.hjenglish.com/fanyijuzi_peter'

def crawl_page(url):
    try:
        html = urllib2.urlopen(url,timeout=10).read()
        soup = BeautifulSoup(html)
        container = soup.find_all('ul', class_ = 'search_result')
        corpussoup = container[0].find_all('li')
        example_sentence = []
        for item in corpussoup:
            en = item.find_all('span', class_ = 'jp_sentence')[0].get_text()
            zh = item.find_all('span', class_ = 'big')[0].get_text()
            example_sentence.append([en,zh])
        return example_sentence
    except:
        print 'Extract page: %s\t failed' %url

def crawl_hujiang(word):
    url = 'http://dict.hjenglish.com/fanyijuzi_' + word
    try:
        html = urllib2.urlopen(url,timeout=10).read()
        soup = BeautifulSoup(html)
        pagesoup = soup.find_all('a', class_ = 'blue')
        lastpage = eval(pagesoup[-1].get_text())
        example_sentence = []
        for i in range(1,lastpage+1):
            suburl = url + '_' + str(i)
            example_sentence.extend(crawl_page(suburl))
        return example_sentence
    except:
        print 'Extract page: %s\t failed' %url
    

dictfile = 'dict.en'
mydict = load_Dict(dictfile)
savefile = codecs.open('hujiang.txt','a+','utf8')
INDEX = 1
itemlist = []
targetindex = 9999999
for item in mydict.keys():
    if INDEX > 1:
        print time.ctime(),INDEX
        itemlist.append(item)
    if len(itemlist) == 20:
        pool = ThreadPool(8)
        result = pool.map(crawl_hujiang, itemlist)
        pool.close()
        pool.join()
        for elelist in result: 
            if elelist != None:
                for ele in elelist:
                    savefile.write(ele[0] + '\n')
                    savefile.write(ele[1] + '\n')
        itemlist = []
    INDEX += 1