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

def seld(list, mode):
    urld(list, mode)

def urld(ani, mode):
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
            print(link)
            if os.path.exists(f'{path}\{aniName}'):
                pass
            else:
                os.system(f"mkdir {path}\{aniName}")

            if mode == 0:
                viddown(name.replace(' ','_').replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|',''), link, aniName, aniLink)
                subdown(name.replace(' ','_').replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|',''), link, aniName, aniLink)
            elif mode == 2:
                viddown(name.replace(' ','_').replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|',''), link, aniName, aniLink)
            elif mode == 1:
                subdown(name.replace(' ','_').replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|',''), link, aniName, aniLink)
    
def viddown(name, URL, folder, anilink):
    print(f'Download {folder} : Starting {name}')

    load = 0
    uri = URL.replace("https://s0.momoafile.info/","").replace(".moe","")  
    headers = {'Referer':URL.encode('utf-8'),'Range':'bytes=0-1'}
    response = requests.get("https://s0.momoafile.info/"+uri+".moe", headers=headers)
    size = int(response.headers['Accept-Ranges'].replace("0-",""))

    if(os.path.exists(path+"/"+folder+"/"+name.replace(" ","_")+".mp4")):
        print(f'Download {folder} : Exists')
        return 0

    download = requests.get("https://s0.momoafile.info/"+uri+".moe", headers=headers)
    f = open(path+"/"+folder+"/"+name.replace(" ","_")+".mp4",'wb')
    f.write(download.content)

    for i in range(0, int(size/1000000-1)):
        head = {'Referer':URL.encode('utf-8'), 'Range':'bytes='+str(i*1000000+2) +"-"+ str((i+1)*1000000+1)}
        f.write(requests.get("https://s0.momoafile.info/"+uri+".moe", headers=head).content)
        lastrange = i + 1
        sys.stdout.write('\r' + f'Download {folder} : Downloading ' + str(int(i*100/int((size/1000000)))) + "%")

    hd = {'Referer':URL.encode('utf-8'), 'Range':'bytes='+str(lastrange*1000000+2) +"-"+ str(size)}
    f.write(requests.get("https://s0.momoafile.info/"+uri+".moe", headers=hd).content)
    sys.stdout.write('\r' + f'Download {folder} : Download Complete\n')
    f.close()

def subdown(name, URL, folder, anilink):
    print(f'Download {folder} : Starting {name}')

    load = 0
    uri = URL.replace("https://s0.momoafile.info/","").replace(".moe","")  
    
    sys.stdout.write('\r' + f'Download {folder} : Subtitle downloading..')
    sb = {'Referer':anilink.encode('utf-8')}
    body = requests.get("https://player.moeni.org/sub.php?v="+uri, headers=sb).content
    if len(body)==0: 
        print()
        sys.stdout.write('\r' + f'Download {folder} : Subtitle Empty..\n')
    else: 
        sub = open(path+"/"+folder+"/"+name.replace(" ","_")+".vtt",'wb')
        sub.write(body)
        sub.close()
        print()
        sys.stdout.write('\r' + f'Download {folder} : Everything Done!\n')

if __name__ == '__main__':
    print("  __  __               _   ___  ___  ___ ")
    print(" |  \/  |___  ___ _ _ (_) / _ \| _ \/ __|")
    print(" | |\/| / _ \/ -_) ' \| || (_) |   / (_ |")
    print(" |_|  |_\___/\___|_||_|_(_)___/|_|_\____|")
    print("")
    print("Downloader for Moeni.ORG Animes")
    print("Made by. Morgan_KR")
    print("\n Selective DOWNLOADER\n")
    db = db_init()
    for i in range(0,len(db)):
        ani = db[i]
        if ani[0] == '':
            pass
        else:
            print(f'{i} : {ani[0]}')
    num = int(input('\n? '))
    mode = input('|(F)ull|(S)ubtitle|(V)ideo| ? ')
    print()
    if mode=="F":
        m = 0
    elif mode=="S":
        m = 1
    elif mode=="V":
        m = 2
    
    seld(db[num], m)
