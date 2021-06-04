from bs4 import BeautifulSoup
import requests
import time
import sys
import os
import urllib
from xml.etree import ElementTree
import re
import bencode
import hashlib
import base64
import sqlite3

def parser(url):

    print('[MoeniMagnet] Parsing')
    mainPage = requests.get(url).content.decode()
    mainPath = mainPage.split('var path=\'')[1].split('\'')[0]
    apiUrl = 'https://player.moeni.org/'
    apiSc = requests.post(apiUrl, data={'path': mainPath, 'host': 'moeni.org'}, headers={'content-type': 'application/x-www-form-urlencoded', 'referer': url,
                          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'})
    apiPage = apiSc.content.decode()
    urll = []
    soup = BeautifulSoup(apiPage, 'html.parser')
    onair = mainPath.split('/')[0]
    title = mainPath.split('/')[1]
    optg = soup.find_all('optgroup')
    if len(optg) == 0:
        for ee in soup.find_all('option'):
            episode = ee.get_text().replace(' ', '')
            if ee.get('value') != None and ee.get('c') != None:
                link1 = ee['value']
                link2 = ee['c']
                url = f'https://player.moeni.org/play.php?c={link2}&v={link1}'
                urll.append({'series': title, 'episode': episode, 'url': url})
    else:
        for opt in optg:
            series = opt['label']
            for ee in opt.find_all('option'):
                episode = ee.get_text().replace(' ', '')
                if ee.get('value') != None and ee.get('c') != None:
                    link1 = ee['value']
                    link2 = ee['c']
                    url = f'https://player.moeni.org/play.php?c={link2}&v={link1}'
                    urll.append(
                        {'series': series, 'episode': episode, 'url': url})
    print("[MoeniMagnet] Parse")
    return(urll, title, onair)

def getMagnet(dict, referer):

    url = dict['url']
    req = requests.get(url, headers={'referer': referer, 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'})
    js = req.content.decode()
    semi_js = js.replace('\r\n', '').split(';')
    llink = semi_js[3].split('f="')[1].split('"')[0]
    llist = eval(semi_js[7].split('=')[1])
    webSeed = llist[11] + 's0.' + llink + llist[13]
    try:
        subUrl = 'https:' + semi_js[18].split('url: "')[1].split('"')[0]
    except:
        subUrl = ''
    magnet = ''
    return magnet, subUrl, webSeed

def main():
	conn = sqlite3.connect("db/magnet.db", isolation_level=None)
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS anime (id integer, bcdate text, name text, url text)")
	c.execute("CREATE TABLE IF NOT EXISTS magnet (id integer , series text,episode text,magnet text,webSeed text,subUrl text,referer text)")
	stmap = []
	sitemap = open('sitemap.xml', 'r')
	smap = BeautifulSoup(sitemap, 'html.parser')
	surl = smap.find_all('url')
	for sss in surl:
		ssurl = sss.get_text()
		if 'https://moeni.org/' in ssurl:
			stmap.append(ssurl)
	start = 0
	for i in range(start, len(stmap)-1):
		url = str(stmap[i])
		print(f"[MoeniMagnet] {i} {url}")
		url_list = parser(url)
		title = url_list[1]
		onair = url_list[2]
		referer = url
		try:
			result = []
			for eplist in url_list[0]:
				ml = getMagnet(eplist, referer)
				magnet = ml[0]
				result.append({'series': eplist['series'], 'episode': eplist['episode'],
							'magnet': magnet, 'webSeed': ml[2], 'sub': ml[1], 'referer': referer})
			c.execute(
				f"INSERT INTO anime VALUES({i+1},'{onair}','{title}','{url}')")
			for res in result:
				c.execute(
					f"INSERT INTO magnet VALUES({i+1}, '{res['series']}','{res['episode']}','{res['magnet']}','{res['webSeed']}','{res['sub']}','{referer}')")
			print('[MoeniMagnet] Complete')
		except Exception as e:
			print(f'getMagnet {e}')

main()