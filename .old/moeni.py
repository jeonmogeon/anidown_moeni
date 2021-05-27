#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import sys
import os

def urld(URL):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("User-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0")
    options.add_argument("lang=ko_KR")

    if  getattr(sys, 'frozen', False): 
        chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
        driver = webdriver.Chrome(chromedriver_path, options=options)
    else:
        driver = webdriver.Chrome(chromedriver, options=options)

    driver.get('about:blank')
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
    driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")
    driver.get(URL)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)
    html = driver.page_source
    driver.quit()
    os.system('cls')
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

    if(os.path.exists(folder+"/"+name.replace(" ","_")+".mp4")):
        if(os.path.getsize(folder+"/"+name.replace(" ","_")+".mp4")==size+1):
            print(os.path.getsize(folder+"/"+name.replace(" ","_")+".mp4")==size+1)
            print("File exists")
            return "Exists"
        else:
            os.system("del "+folder+"/"+name.replace(" ","_")+".mp4")   
            print("File exists but suspended. Re-downloading...")

    print("Download Start")
    download = requests.get("https://s0.momoafile.info/"+uri+".moe", headers=headers)
    f = open(folder+"/"+name.replace(" ","_")+".mp4",'wb')
    f.write(download.content)

    for i in range(0, int(size/1000000-1)):
        head = {'Referer':URL.encode('utf-8'), 'Range':'bytes='+str(i*1000000+1) +"-"+ str((i+1)*1000000)}
        f.write(requests.get("https://s0.momoafile.info/"+uri+".moe", headers=head).content)
        lastrange = i + 1
        sys.stdout.write('\r' + "Downloading " + str(int(i*100/int((size/1000000)))) + "%")

    hd = {'Referer':URL.encode('utf-8'), 'Range':'bytes='+str(lastrange*1000000+1) +"-"+ str(size)}
    f.write(requests.get("https://s0.momoafile.info/"+uri+".moe", headers=hd).content)
    sys.stdout.write('\r' + "Downloading Complete")
    f.close()
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
    print()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: moeni.exe [URL]")
        sys.exit()
    else:
        URL = sys.argv[1]
        print("  __  __               _   ___  ___  ___ ")
        print(" |  \/  |___  ___ _ _ (_) / _ \| _ \/ __|")
        print(" | |\/| / _ \/ -_) ' \| || (_) |   / (_ |")
        print(" |_|  |_\___/\___|_||_|_(_)___/|_|_\\____|")
        print("")
        print("Downloader for Moeni.ORG Animes")
        print("Made by. Morgan_KR")
        urld(URL)