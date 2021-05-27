#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import pymysql

path = "downloads"

conn = pymysql.connect(*)
curs = conn.cursor()
    
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

def urld(ani, ina):
    if ani[0] == '':
        pass
    else:
        aniLink = ani[1]
        aniName = aniLink.replace('https://moeni.org/','').replace('/','').replace('-',' ')
        epiList = ani[2]
        print(f'Download {aniName} : Total {len(epiList)}\n')
        for episode in epiList:
            name = episode[0]
            link = episode[1]
            file = name.replace(' ','_').replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|','')
            ll = aniName.replace(' ','_').replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|','')
            print(file.split(ll)[0])
                        
                
def dba(ind, sp, ep, name, URL, folder, anilink):
    sql = f'INSERT INTO aniInfo(id,file,sp,ep,uri) VALUES ({ind},"{name}",{sp},{ep},"{URL.replace("https://s0.momoafile.info/","").replace(".moe","")}")'
    print(sql)
    curs.execute(sql)
    conn.commit()
 
if __name__ == '__main__':
    print("  __  __               _   ___  ___  ___ ")
    print(" |  \/  |___  ___ _ _ (_) / _ \| _ \/ __|")
    print(" | |\/| / _ \/ -_) ' \| || (_) |   / (_ |")
    print(" |_|  |_\___/\___|_||_|_(_)___/|_|_\____|")
    print("")
    print("Downloader for Moeni.ORG Animes")
    print("Made by. Morgan_KR")
    print("\n Full DOWNLOADER\n")
    db = db_init()
    ind = 1
    for ani in db:
        urld(ani, ind)
        ind+=1
    conn.close()

