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

def urld(URL, f, n):
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
    print(URL)
    print(folder)
    for i in range(5, len(opt)):
        print("Checking " + opt[i].get('sel'))
        down(opt[i].get('sel'),opt[i].get('value'),URL,folder,f,n)

def down(name, uri,URL,folder, f, n):
    f.write(str(n)+"@"+folder+"@"+name+"@"+URL+"@"+"https://s0.inefile.xyz/"+uri+".moe\n")
    print(str(n)+"@"+folder+"@"+name+"@"+URL+"@"+"https://s0.inefile.xyz/"+uri+".moe")
  
def auto_sitemap():
    f = open("db.lsd", "w")
    site = open("sitemap.xml", 'r', -1, 'utf-8')
    print("Sitemap Loaded")
    xml = site.read()
    soup = BeautifulSoup(xml, 'html.parser')
    url = []
    for loc in soup.find_all("loc"):
       url.append(loc.text)
    
    for i in range(0,len(url)-1):
        try:
            urld(url[i],f, i+1)
        except Exception as e:
            f.write("Failed")
            print(f"Failed\n--> {e}")
    
    f.close   
def sitemap():
    sitemap = open('sitemap.xml', 'wb')
    sitereq = requests.get('https://moeni.org/sitemap.xml')
    sitemap.write(sitereq.content)
    sitemap.close()
    print("Sitemap Downloaded")

if __name__ == '__main__':
    print("  __  __               _   ___  ___  ___ ")
    print(" |  \/  |___  ___ _ _ (_) / _ \| _ \/ __|")
    print(" | |\/| / _ \/ -_) ' \| || (_) |   / (_ |")
    print(" |_|  |_\___/\___|_||_|_(_)___/|_|_\\____|")
    print("")
    print("Downloader for Moeni.ORG Animes")
    print("Made by. Morgan_KR")
    sitemap()
    auto_sitemap()
