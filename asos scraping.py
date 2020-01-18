# libraries

import zipfile
import os
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
from bs4 import Comment
import requests
import io
import hashlib
from PIL import Image #pip install Pillow

# CLINKING ON THE SPECIFIC ELEMENT TO LOAD MORE CONTENT UNTIL REACH THE LAST PAGE
# LINK YOU WANT TO START SCRAPING, in this case we are going to scrape dresses
link = 'https://www.asos.com/women/dresses/cat/?cid=8799&nlid=ww|clothing|shop+by+product'
# PATH TO YOU WEBDRIVER
driver = webdriver.Chrome("chromedriver 79")
driver.get(link)
Number = 300 # JUST A BIG NUMBER
for i in range(Number): 
    try:
        try:
            elem = driver.find_element_by_xpath('/html/body/main/div/div/div/div[2]/div/a')
            elem.click()
        except:
            time.sleep(10)
            elem = driver.find_element_by_xpath('//*[@id="plp"]/div/div/div[2]/div/a')
            elem.click()
    except:
        try:
            elem = driver.find_element_by_xpath('/html/body/main/div/div/div/div[2]/div/a')
            elem.click()
        except:
            time.sleep(10)
            elem = driver.find_element_by_xpath('//*[@id="plp"]/div/div/div[2]/div/a')
            elem.click()


# GETTING PRODUCT LINKS
product_links = [x.get_attribute('href') for x in driver.find_elements_by_css_selector("article a")]

#OPTIONAL, IF YOU WANT YOU CAN SAVE THEM 
with open('links/links.txt', 'w') as f:
    for link in product_links:
        f.write("%s\n" % link)

# ELEMENT WE ARE ABOUT OT SAVE
pic_links =[]
prod_links=[] 
description=[]

# POSITION OF IMAGES ON THE WEB
pics =['//*[@id="product-gallery"]/div[1]/div[2]/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div[1]/img',
       '//*[@id="product-gallery"]/div[1]/div[2]/div[3]/div/div/div/div[1]/div[1]/div[3]/div/div/img',
       '//*[@id="product-gallery"]/div[1]/div[2]/div[4]/div/div/div/div[1]/div[1]/div[3]/div/div/img',
       '//*[@id="product-gallery"]/div[1]/div[2]/div[5]/div/div/div/div[1]/div[1]/div[3]/div/div/img']
#COUNTRER
k=0
# GETTING DESCRIPTION AND PIC'S LINK
for link in product_links:
    if k%100==0:
        print(k)
    k+=1
    driver.get(link)
    try:
        try:
            prod_links.append(link)
            time.sleep(5)
            #pressing botton
            elem = driver.find_element_by_xpath('/html/body/main/div[1]/section[2]/div/div/div/div[4]/div/a[1]')
            elem.click()
            det = driver.find_element_by_xpath('//*[@id="product-details"]/div/div[1]/div/ul')
            description.append(det.text.split('\n'))
            enlace = []
            for i in range(4):
                elem = driver.find_element_by_xpath(pics[i])
                enlace.append(elem.get_attribute('src'))
                elem = driver.find_element_by_xpath('//*[@id="product-gallery"]/div[1]/button[1]/div')
                elem.click()
            pic_links.append(enlace)
        except:
            elem = driver.find_element_by_xpath('//*[@id="aside-content"]/div[1]/h3')
            if elem.text=='OUT OF STOCK':
                pass
    except:
        try:
            prod_links.append(link)
            time.sleep(5)
            #pressing botton
            elem = driver.find_element_by_xpath('/html/body/main/div[1]/section[2]/div/div/div/div[4]/div/a[1]')
            elem.click()
            det = driver.find_element_by_xpath('//*[@id="product-details"]/div/div[1]/div/ul')
            description.append(det.text.split('\n'))
            enlace = []
            for i in range(4):
                elem = driver.find_element_by_xpath(pics[i])
                enlace.append(elem.get_attribute('src'))
                elem = driver.find_element_by_xpath('//*[@id="product-gallery"]/div[1]/button[1]/div')
                elem.click()
            pic_links.append(enlace)
        except:
            elem = driver.find_element_by_xpath('//*[@id="aside-content"]/div[1]/h3')
            if elem.text=='OUT OF STOCK':
                pass
    else:
        pass


# DOWNLOADING IMAGES BY URL

def persist_image(folder_path:str,url:str):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


[persist_image('/pictures', pic) for pic in pic_links]

#CREATING AND SAVING CSV WITH SCRAPED INFO
df = pd.DataFrame({'production links': prod_links, 'pic description': description, 'picture link':pic_links}
df.to_csv('scraped_info')