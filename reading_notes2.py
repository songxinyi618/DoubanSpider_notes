# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 13:47:02 2018

@author: Administrator
"""
from selenium import webdriver
from bs4 import BeautifulSoup

from urllib import request
from urllib.request import urlretrieve

import os
import time
import pandas as pd 
import csv

head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'} 

###########################提取book_info#######################################
filepath = 'E:/宋心艺/book_json/book_json.csv'

pwd = os.getcwd()
os.chdir(os.path.dirname(filepath))
data = pd.read_csv(os.path.basename(filepath),encoding = 'utf-8')
#print(data)
book_info = pd.DataFrame({'bookname':data['bookname'],'ISBN':data['ISBN']})
#print(book_info)

#########################打印前几页读书笔记的URL#####################################
def get_annotation_url(annotation_url, head,book_name):
    #annotation_url = 'https://book.douban.com/subject/4890389/annotation'
    annotation_req = request.Request(url = annotation_url, headers = head)
    annotation_response = request.urlopen(annotation_req)
    annotation_html = annotation_response.read().decode('utf-8','ignore')
    annotation_soup = BeautifulSoup(annotation_html , 'lxml')
    annotation_paginator = annotation_soup.find('div',{'class':'paginator'})
    #print(annotation_paginator)
    annotation_contents = []
    #print(annotation_list)
    comments = annotation_soup.find('ul',{'class':'comments by_rank'}).contents
    #print(comments)
    try:    
        for child in enumerate(annotation_paginator.contents):
        #print(annotation_paginator.contents[21].string) 
            if child[1].string != '\n':
                annotation_contents.append(child[1])
   
#annotation_contents = list(filter(lambda x: x != None, annotation_contents))
#print(annotation_contents)[0:12]).name)['class'])

        annotation_list = [annotation_url]
      
        for child in annotation_contents:   
        #print(child.name,child.attrs)
            if child.attrs == {'class': ['prev']} or child.attrs == {'class': ['thispage']} or child.attrs == {'class': ['next']}:
            #print(child)
               continue
   
            elif child.attrs == {'class': ['break']}:
                break
            href = book_url + 'annotation' +child.get('href')
            annotation_list.append(href)
        #print(annotation_list) 
        print(book_name,'有多页')
        
    except:
        if comments == ['\n']:
            print(book_name,'没有读书笔记')
            annotation_list = []
            
        else :
            print(book_name,'有1页读书笔记')
            annotation_list = [annotation_url]
            
    return annotation_list
########################爬取用户头像图片########################################
def get_user_img(annotation_list, head):

    for one in annotation_list:
        filepath2 = 'E:/宋心艺/Github/爬虫学习/'
        os.chdir(os.path.dirname(filepath2))
        
        #one = 'https://book.douban.com/subject/11601218/annotation?sort=rank'
        img_req = request.Request(url = one, headers = head)
        img_response = request.urlopen(img_req)
        img_html = img_response.read().decode('utf-8','ignore')
        img_soup = BeautifulSoup(img_html , 'lxml')
        img_ilst = img_soup.find_all('div',{'class':'ilst'})  
        #print(img_ilst)
        for each in img_ilst:
            img_url = each.img.get('src')
            filename = each.img.get('alt') + '.jpg'
        #list_url.append(each.img.get('src'))
        #print(list_url)
            if 'images2' not in os.listdir():
                os.makedirs('images2')
            try:
                urlretrieve(url = img_url,filename = 'images2/' + filename)
            except:
                print(filename,'下载头像失败')
            time.sleep(1)    
            
########################爬取用户读书笔记内容####################################
def get_location_notes(annotation_list, head,book_name):
    reading_notes = []

    for one in annotation_list:
        reading_req = request.Request(url = one, headers = head)
        reading_response = request.urlopen(reading_req)
        reading_html = reading_response.read().decode('utf-8','ignore')
        reading_soup = BeautifulSoup(reading_html , 'lxml')
        reading_con = reading_soup.find_all('div',{'class':'con'}) 
        #print(reading_con)
        for each in reading_con:
            location = each.find('a',{'class':''}).string #print(location)
            all_hidden = each.find('div',{'class':'all hidden','style':'display:none'}).get_text()#print(all_hidden)
            notes = all_hidden.split('推荐')[0]#
            #print(notes)
        
            sdata = {'location':location,'notes':notes}
            reading_notes.append(sdata)
    reading_notes = pd.DataFrame(reading_notes)#print(reading_notes[1:7])
    
    reading_path = '%s%s%s' %('E:\宋心艺\Github\爬虫学习\读书笔记2\\', book_name, '.csv') #print(reading_path)
    reading_notes.to_csv(reading_path, index = False,encoding = 'utf-8')

######################调用子函数###############################################
if __name__=='__main__':
    for i in range(0,175):
        browser = webdriver.Firefox()
        browser.get('https://book.douban.com/')
         
        one = book_info.loc[i]
        #print(one)
        ISBN = one['ISBN']
        book_name = one['bookname']
        #print(ISBN,book_name)
        
        keyword = browser.find_element_by_id('inp-query')
        keyword.send_keys(str(ISBN))#关键词在此
        
        button = browser.find_element_by_class_name('inp-btn')
        button.click()#点击搜索框
        try:
            link = browser.find_element_by_class_name('title-text')
            book_url = link.get_attribute('href')
            annotation_url = book_url +"annotation?sort=rank"
        #print(book_url)
        except:
            print(book_name,'没有对应的ISBN号')
############ 
        #annotation_url = 'https://book.douban.com/subject/4890389/annotation'
        annotation_list = get_annotation_url(annotation_url, head,book_name)

############ 
        if annotation_list != []:
            try:
                get_user_img(annotation_list, head)
                print(book_name,'下载头像成功')
            except:
                print(book_name,'下载头像失败')           
            try:
                get_location_notes(annotation_list, head,book_name)
                print(book_name,'读书笔记成功')
            except:
                print(book_name,'读书笔记失败')
        
        time.sleep(30)
        #keyword.clear()  
        #sreach_window=browser.current_window_handle#切换到新页面
        browser.close()
        


