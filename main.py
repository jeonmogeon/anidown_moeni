#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import sys
import os
import urllib
from xml.etree import ElementTree
import re
import chromedriver_autoinstaller
import bencode
import hashlib
import base64
import sqlite3

def chwd(URL):
	print("[MoeniMagnet] Driver Start")
	chromedriver_autoinstaller.install()
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('window-size=1920x1080')
	options.add_argument("disable-gpu")
	options.add_argument("User-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0")
	options.add_argument("lang=ko_KR")
	driver = webdriver.Chrome('chromedriver', options=options)
	print("[MoeniMagnet] Driver Init")
	driver.get(URL)
	print("[MoeniMagnet] Driver Get")
	driver.switch_to.window(driver.window_handles[0])
	time.sleep(1)
	html = driver.page_source
	urrl = driver.current_url
	driver.quit()
	return(html,urrl)
		
def parser(html):
	soup = BeautifulSoup(html, 'html.parser')
	print('[MoeniMagnet] Parsing')
	urll = []
	title = soup.find('div','info_name').get_text().replace('\n','')
	for p in soup.find('div','player').find_all('p'):
		for ee in p.find_all('a'):
			episode = ee.get_text()
			link1 = ee['onclick'].split('load("')[1].split('",$')[0]
			link2 = ee['c']
			url = f'https://player.moeni.org/play.php?c={link2}&v={link1}'
			urll.append({'episode':episode,'url':url})
	return(urll, title)
	
def getMagnet(dict,referer):
	url = dict['url']
	req = requests.get(url, headers={'referer':referer,'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'})
	js = req.content.decode()
	semi_js = js.replace('\r\n','').split(';')
	llink = semi_js[3].split('f="')[1].split('"')[0]
	llist = eval(semi_js[7].split('=')[1])
	webSeed = llist[10] + 's0.' + llink + llist[12]
	subUrl = 'https:' + semi_js[18].split('url: "')[1].split('"')[0]
	torUrl = eval(semi_js[20].split('videoId = ')[1])

	# print(webSeed, subUrl, torUrl)

	req = requests.get(torUrl, headers={'referer':referer,'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'})

	metadata = bencode.bdecode(req.content)
	hashcontents = bencode.bencode(metadata['info'])
	digest = hashlib.sha1(hashcontents).digest()
	b32hash = base64.b32encode(digest)
	magnet = f'magnet:?xt=urn:btih:{b32hash.decode()}&dn={requests.utils.quote(metadata["info"]["name"])}&ws={requests.utils.quote(webSeed)}&tr={requests.utils.quote("wss://tracker.inefile.xyz")}'
	return magnet, subUrl, webSeed


conn = sqlite3.connect("db/magnet.db", isolation_level=None)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS anime (id integer PRIMARY KEY, name text, url text)")
c.execute("CREATE TABLE IF NOT EXISTS magnet (id integer , episode text,magnet text,webSeed text,subUrl text,referer text)")

stmap = []
sitemap = open('sitemap.xml','r')
smap = BeautifulSoup(sitemap, 'html.parser')
surl = smap.find_all('url')
for sss in surl:
	ssurl= sss.get_text()
	if 'https://moeni.org/' in ssurl:
		stmap.append(ssurl)
		# name = requests.utils.unquote(ssurl)
		# print(name.split('https://moeni.org/')[1].replace('-',' ').replace('/',''))

#####################
start = 1
#####################

for i in range(start,len(stmap)-1):
	url = str(stmap[i])
	print(f"[MoeniMagnet] #{i} {url}")
	chwdr = chwd(url)
	url_list = parser(chwdr[0])
	title = url_list[1]

#	for i in url_list[0]:
#		print(f"[MoeniMagnet] [{title}] {i['episode']}")

	referer = chwdr[1] 
	try:
		result = []
		for eplist in url_list[0]:
			ml = getMagnet(eplist,referer)
			magnet = ml[0]
			result.append({'episode':eplist['episode'],'manget':magnet,'webSeed':ml[2],'sub':ml[1],'referer':referer})
		#print(result)
		c.execute(f"INSERT INTO anime VALUES({i}, '{title}','{url}')")
		for res in result:
			c.execute(f"INSERT INTO magnet VALUES({i}, '{res['episode']}','{res['magnet']}','{res['webSeed']}','{res['sub']}','{referer}')")
			print('DBIN')
	except Exception as e:
		print(e)