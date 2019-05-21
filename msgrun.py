import requests
from bs4 import BeautifulSoup 
import itchat

from lxml.html import etree
import os
import pymysql
import random
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

import json
import time
from time import sleep

#from Config import * 
import logging
import datetime

global rows
global values
url = 'http://finance.sina.com.cn/7x24/?tag=0'
basedir = os.path.dirname(os.path.realpath(__file__))
logfile = "%s\\log\\sina_%s.log" % (basedir, datetime.datetime.now().strftime("%Y-%m-%d"))
logging.basicConfig(filename = logfile, level = logging.DEBUG, format = '%(asctime)s  %(message)s')

logfilename = "%s\\DATA\\sina_%s.sql" % (basedir, datetime.datetime.now().strftime("%Y-%m-%d"))

start = time.time()
infor = "Import all  stocks begins!"
logging.info(infor)
rows = 0
values = []
header = "INSERT INTO `sina_news` (`n_date`, `n_time`, `content`) VALUES"
middle = "(%s, %s, %s)"

query = header + middle

usernameUsed = ''
#!!!update your NickName!!!
searchNickName='XXXXX' 

def sina():
        is_first = True
        task_q = []
        task_time = []
        checkTime = 0
        lastCheckTime = 0
        firstTime = True
        while True:
                

            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            driver = webdriver.Chrome(chrome_options = options, executable_path = '/usr/bin/chromedriver')
            driver.implicitly_wait(30)
            driver.maximize_window()
            
            driver.implicitly_wait(10)
            # driver.maximize_window()
            driver.set_page_load_timeout(30)
            try:
                driver.get(url)
                checkTime = time.time()
                # sroll_multi(driver)
                data_secs = driver.find_elements_by_xpath('//*[@id="liveList01"]/div')
            except TimeoutException:
                print('timeout11...')
                #driver.execute_script('window.stop()')
                driver.close()
                continue
            
            for data_sec in data_secs:
                    try: 
                        day = data_sec.get_attribute('data-time')
                        hour_min = data_sec.find_element_by_class_name('bd_i_time_c')
                        content = data_sec.find_element_by_class_name('bd_i_txt_c')
                        #print(day, content.text, hour_min)
                        data_time = time.mktime(datetime.datetime.strptime(day + ' ' + hour_min.text, "%Y%m%d %H:%M:%S").timetuple())
                        #print(firstTime, data_time, checkTime, lastCheckTime, '@@')
                        if (data_time > lastCheckTime):
                            print('eeee')
                            itchat.send('New Message: ' + day + ' ' + hour_min.text + '---' + content.text, toUserName = usernameUsed)
                        # filename = "%s\\data\\sina24x_%s.txt" % (basedir, day)
                
                        # value = [day, hour_min.text, content.text]
                        # filecontent = hour_min.text + '\t' + content.text# write_content_to_file(filename, filecontent)
                        # values.append(value)
                        
                        # rows = rows + 1
                        #if (rows % 50 == 0): 
                            #insert_query(query, values)
                            # values = []
                        #if len(values) > 0: 
                            #insert_query(query, values)
                            # values = []
                    except TimeoutException:
                        print('timeout22...')
                        break
                    
                    
            #driver.execute_script('window.stop()')   
            driver.close()   
            time.sleep(60)

            lastCheckTime = checkTime
            firstTime = False

itchat.auto_login()
all = itchat.get_friends()
for i in all:
    if i.NickName==searchNickName:
        print('get the username: ', i.UserName)
        usernameUsed = i.UserName

sina()
