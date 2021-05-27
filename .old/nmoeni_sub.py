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

path = "downloads"

def db_init():
    dbfile = open('./db.lsd', 'r', -1, 'utf-8')
    print("Database Loaded")
    data = dbfile.readlines()
    DB = []
    for i in range(0,1200):
        DB.append('')
        DB[i] = ['','',[]]
    # no @ aniname @ filename @ anilink @ vidlink
    for list in data:
        if list == "ERROR\n":
            pass
        else:
            no = int(list.split('@')[0])
            aniName = list.split('@')[1]
            aniLink = list.split('@')[3]
            
            vidLink = list.split('@')[2].replace('\n','')
            fileName = list.split('@')[4].replace('\n','')

            DB[no][0] = aniName
            DB[no][1] = aniLink
            DB[no][2].append([vidLink, fileName])
    
    print("Database returned to ARRAY\n")
    return(DB)

def urld(ani):
    if ani[0] == '':
        pass
    else:
        aniName = ani[0]
        aniLink = ani[1]
        epiList = ani[2]
        print(f'Download {aniName} : Total {len(epiList)}\n')
        for episode in epiList:
            name = episode[0]
            link = episode[1]
            if os.path.exists(f'{path}\{aniName}'):
                pass
            else:
                os.system(f"mkdir {path}\{aniName}")

            down(name.replace(' ','_').replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|',''), link, aniName)
    
def down(name, URL, folder):
    print(f'Download {folder} : Starting {name}')

    load = 0
    uri = URL.replace("https://s0.inefile.xyz/","").replace(".moe","")  
    
    sys.stdout.write('\r' + f'Download {folder} : Subtitle downloading..')
    sb = {'Referer':URL.encode('utf-8')}
    body = requests.get("https://player.moeni.org/sub.php?v="+uri, headers=sb).content
    if len(body)==0: 
        sys.stdout.write('\r' + f'Download {folder} : Subtitle Empty..\n')
    else: 
        sub = open(path+"/"+folder+"/"+name.replace(" ","_")+".vtt",'wb')
        sub.write(body)
        sub.close()
        sys.stdout.write('\r' + f'Download {folder} : Everything Done!\n')
 
if __name__ == '__main__':
    print("  __  __               _   ___  ___  ___ ")
    print(" |  \/  |___  ___ _ _ (_) / _ \| _ \/ __|")
    print(" | |\/| / _ \/ -_) ' \| || (_) |   / (_ |")
    print(" |_|  |_\___/\___|_||_|_(_)___/|_|_\____|")
    print("")
    print("Downloader for Moeni.ORG Animes")
    print("Made by. Morgan_KR")
    print("\n SUBTITLE DOWNLOADER\n")
    db = db_init()
    for ani in db:
        urld(ani)