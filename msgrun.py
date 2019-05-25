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
#通过下面的方式进行简单配置输出方式与日志级别
import logging
import datetime

from itchat.content import *
import _thread

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

requestcmd='detail'

def sina():
        global requestcmd
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
                        classValue = data_sec.get_attribute('class')
                        #print(day, content.text, hour_min)
                        data_time = time.mktime(datetime.datetime.strptime(day + ' ' + hour_min.text, "%Y%m%d %H:%M:%S").timetuple())
                        #print(firstTime, data_time, checkTime, lastCheckTime, '@@')
                        if (data_time > lastCheckTime and 'bd_i_focus' in classValue and requestcmd=='simple'):
                            print('sss')
                            itchat.send('New Message: ' + day + ' ' + hour_min.text + '---' + content.text, toUserName = usernameUsed)
                        elif (data_time > lastCheckTime and requestcmd=='detail'):
                            print('ddd')
                            itchat.send('New Message: ' + day + ' ' + hour_min.text + '---' + content.text, toUserName = usernameUsed)
                        elif (data_time > lastCheckTime and requestcmd=='close'):
                            print('stop sending')

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

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    global requestcmd
    #msg.user.send('%s: %s' % (msg.type, msg.text))
    #print(msg.text, requestcmd)
    msgret = ''
    if (msg.text=='detail'):
        msgret = 'detail model select'
    elif (msg.text=='simple'):
        msgret = 'simple model select'
    elif (msg.text=='close'):
        msgret = 'the message will not be sent'
        
    if len(msgret):
        print(msgret)
        requestcmd = msg.text
        msg.user.send(msgret)


itchat.auto_login()
all = itchat.get_friends()

for i in all:
    if i.NickName==searchNickName:
        print('get the username: ', i.UserName)
        usernameUsed = i.UserName

itchat.start_receiving()

#sina()

try:
   _thread.start_new_thread( sina, () )
   #thread.start_new_thread( print_time, ("Thread-2", 4, ) )
except e:
   print("Error: unable to start thread", e)

itchat.run()

