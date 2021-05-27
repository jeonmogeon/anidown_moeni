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

def urld(URL):
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
    folder = opt[5].get('sel').replace(" 01화","").replace(" ","_")
    os.system("mkdir "+folder+"")
    for i in range(5, len(opt)):
        print("Checking " + opt[i].get('sel'))
        down(opt[i].get('sel'),opt[i].get('value'),URL,folder)

def down(name, uri,URL,folder):
    load = 0  
    headers = {'Referer':URL.encode('utf-8'),'Range':'bytes=0-0'}
    # print("https://s0.momoafile.info/"+uri+".moe")
    response = requests.get("https://s0.momoafile.info/"+uri+".moe", headers=headers)
    size = int(response.headers['Accept-Ranges'].replace("0-",""))

    if(os.path.exists(folder+"/"+name.replace(" ","_")+".vtt")):
        print("Exists")
        return 0

    print("Subtitle downloading..")
    sb = {'Referer':URL.encode('utf-8')}
    body = requests.get("https://player.moeni.org/sub.php?v="+uri, headers=sb).content
    if len(body)==0: 
        print("Empty..")
    else: 
        sub = open(folder+"/"+name.replace(" ","_")+".vtt",'wb')
        sub.write(body)
        sub.close()
        print("Done!")
    
def auto_sitemap():
    site = open("vsitemap.xml", 'r')
    print("Sitemap Loaded")
    xml = site.read()
    soup = BeautifulSoup(xml, 'html.parser')
    url = []
    for loc in soup.find_all("loc"):
       url.append(loc.text)
    
    for i in range(0,len(url)-1):
        try:
            urld(url[i])
        except Exception:
            print("Failed")     
        
if __name__ == '__main__':
    print("  __  __               _   ___  ___  ___ ")
    print(" |  \/  |___  ___ _ _ (_) / _ \| _ \/ __|")
    print(" | |\/| / _ \/ -_) ' \| || (_) |   / (_ |")
    print(" |_|  |_\___/\___|_||_|_(_)___/|_|_\\____|")
    print("")
    print("Downloader for Moeni.ORG Animes")
    print("Made by. Morgan_KR")
    auto_sitemap()
    # urld("https://moeni.org/%EB%A7%88%EC%99%95%ED%95%99%EC%9B%90%EC%9D%98-%EB%B6%80%EC%A0%81%ED%95%A9%EC%9E%90/")
