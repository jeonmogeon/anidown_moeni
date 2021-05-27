#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import sys
import os
from xml.etree import ElementTree
import re
import chromedriver_autoinstaller

def urld(URL):
    chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("User-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0")
    options.add_argument("lang=ko_KR")
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get('about:blank')
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
    driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")
    driver.get(URL)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')
    opt = soup.find_all("option")
    folder = opt[5].get('sel').replace(" 01화","").replace(" ","_").replace(",","").replace(")","").replace("(","").replace("","")
    os.system("mkdir "+folder+"")
    for i in range(5, len(opt)):
        print(str(i) + " : " + opt[i].get('sel'))

    print()
    s = input("? ")
    print()
    down(opt[int(s)].get('sel'),opt[int(s)].get('value'),URL,folder)
        
urld("https://moeni.org/%EB%A7%88%EC%99%95%ED%95%99%EC%9B%90%EC%9D%98-%EB%B6%80%EC%A0%81%ED%95%A9%EC%9E%90/")
