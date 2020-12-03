# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 21:07:13 2020

@author: kbzg512
"""

###########################
###########################
#
# Generates Redshift compliant SQL. Don't ask why.
# But- ths imports into 
# 
###########################
###########################



url = 'https://help.sap.com/viewer/4fe29514fd584807ac9f2a04f6754767/2.0.03/en-US/20a380977519101494ceddd944e87527.html'

    
BASE_URL = 'https://help.sap.com/viewer/4fe29514fd584807ac9f2a04f6754767/2.0.03/en-US/'
SUFFIX_URL = ".html"

table = '209e0cde751910149114be53649a1fb7'

url = str(BASE_URL + '/' + table + '/' + table + SUFFIX_URL )

print(url)



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from html import escape  

import time

DRIVER_PATH="C:\\Users\\kbzg512\\OneDrive - AZCollaboration\\Useful\\Software\\chromedriver\\chromedriver.exe"
WORKING_DIR= "C:\\Users\\kbzg512\\OneDrive - AZCollaboration\\Personal\\python\\hana_grammar\\"


OUTPUT_DIR=WORKING_DIR+"raw_html\\"

options = Options()
options.headless = False
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://www.google.com")

driver.get(url)

#driver.quit()



  
def get_bnf_data_pages(driver):
    
element_title = driver.find_element_by_xpath('//*/h1')
title = element_title.text

while title != 'Aggregate Functions':
           
    file_name = escape(title) + ".html"
    
    src = driver.page_source
    
    # Write the src data out to a file.         
    with open(OUTPUT_DIR +file_name, 'w',encoding='utf-8') as f:
       f.write(src)  

    # Navigate to the next page. 
    #element_next = driver.find_element_by_xpath('//*[@id="toc-next"]/span')
    element_next = driver.find_element_by_xpath("//*[contains(text(), 'Next')]")
    element_next.click()

    time.sleep(30)
    
    # Get the title of the new page. 
    #element_title = driver.find_element_by_class_name('title topictitle1')
    element_title = driver.find_element_by_xpath('//*/h1')
    title = element_title.text
    
    print(title)

        
        
        



