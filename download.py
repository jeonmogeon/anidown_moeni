import requests
import sqlite3, re, os
import time
import asyncio
import aiohttp
import aiofiles
import aiodns

PATH = 'downloads'
TMP_PATH = 'downloads/tmp'
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'
epist = {}
anime = {}

def db_call():
    global magnet
    global anime
    conn = sqlite3.connect("db/magnet.db") 
    cur = conn.cursor() 

    cur.execute(f"SELECT id, name FROM anime") 
    rows = cur.fetchall() 
    for row in rows: 
        id = row[0]
        name = row[1]
        anime[id] = name
        epist[id] = []

    cur.execute("SELECT * FROM magnet") 
    rows = cur.fetchall() 
    for row in rows: 
        id = row[0]
        series = row[1]
        episode = row[2]
        magnet = row[3]
        webseed = row[4]
        suburl = row[5]
        referer = row[6]
        epist[id].append({'series':series,'episode':episode,'magnet':magnet,'webseed':webseed,'suburl':suburl,'referer':referer})

def seedPiece(url, ref, fname, name):
    startT = time.time()
    blocksize = 3000000
    size = requests.get(url, headers={'referer':ref,'range':f'bytes=0-1','user-agent':ua}).headers['Content-Range'].split(' ')[1].split('/')[1]
    blockC = int(int(size)/blocksize)
    print(f'Total {size}')
    if not os.path.exists(os.path.join(PATH,name)):
        os.mkdir(os.path.join(PATH,name))

    ds = [downseed(i, blocksize, blockC,url,ref,fname,size,name) for i in range(0,blockC+1)]
    asyncio.run(asyncio.wait(ds))
    mergeFile(fname, blockC, size, name)
    try:
        print(f'\nTime:{int(time.time() - startT)}s, Size:{int(int(size)/(1024*1024))}MB, Speed: {round( int(int(size)/(1024*1024)) / int(time.time() - startT), 2)}MB/s')
    except:
        pass
    print('')

async def downseed(i, blocksize, blockC,url,ref,fname,size,name):
    start = i*blocksize
    if i == blockC:
        end = size
    else:
        end = (i+1)*blocksize-1
    # print(f'{start} to {end}')
    # if os.path.exists(os.path.join(PATH,f'{fname}.part{i}')):
    #     if os.path.getsize(os.path.join(PATH,f'{fname}.part{i}')) == blocksize:
    #         print(f'{os.path.join(PATH,f"{fname}.part{i}")} EXIST')
    if os.path.exists(os.path.join(os.path.join(PATH,name),f'{fname}.mp4')):
            if os.path.getsize(os.path.join(os.path.join(PATH,name),f'{fname}.mp4')) == int(size):    
                return(0)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={'referer':ref,'range':f'bytes={start}-{end}','user-agent':ua}) as resp:
                async with aiofiles.open(os.path.join(TMP_PATH,f'{fname}.part{i}'), 'wb') as f:
                    await f.write(await resp.read())
                    # print(resp.read())
                    print(f'|',end='')

    except Exception as e:
        print(e)
        return 'e'

def mergeFile(fname, blockC, size, name):
    if os.path.exists(os.path.join(os.path.join(PATH,name),f'{fname}.mp4')):
        if os.path.getsize(os.path.join(os.path.join(PATH,name),f'{fname}.mp4')) == int(size):  
            return(0)  
            print("AE\r",end='')

    try:
        with open(os.path.join(os.path.join(PATH,name),f'{fname}.mp4'), 'wb') as f:
            for i in range(0,blockC+1):
                with open(os.path.join(TMP_PATH,f'{fname}.part{i}'), 'rb') as tmp:
                    f.write(tmp.read())
                os.remove(os.path.join(TMP_PATH,f'{fname}.part{i}'))
    except:
        print("E\r")

def sub(url, ref, s):
    try:
        req = requests.get(url, headers={'referer':ref,'user-agent':ua})
        #print(req.content)
        #print(req.headers)
        if req.status_code == 200:
            s.write(req.content)
            print(f'Complete: SUB')
        else:
            raise f'FetchError {req.status_code}'
    except Exception as e:
        print(e)

def epi(name, id, info):
    fname = re.sub('[-=+,#/\?:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]','',f"{name}_{info['series']}_{info['episode'].replace(' ','_')}")
    sname = re.sub('[-=+,#/\?:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]','',f"{name}_{info['series']}_{info['episode'].replace(' ','_')}")
    url = info['webseed'].replace('https','http')
    subU = info['suburl']#.replace('https','http')
    ref = info['referer']

    print(f'Downloading {fname}')
    seedPiece(url, ref, fname, name)

    # print(f'Downloading {sname}')
    # s = open(os.path.join(PATH,sname+'.vtt'), 'wb')
    # sub(subU, ref, s)
    # s.close()

db_call()

for id in anime:
    name = anime[id]
    f = open('loag.ee','r')
    buf = f.read()
    f.close()

    if str(id) in buf:
        print(f"{id} Already Done")
        continue
        
    for info in epist[id]:
        epi(name, id, info)
    with open('loag.ee','a') as f:
        f.write(f'{id}\n')
