import urllib.request as urlreq
import urllib.error as urlerr
from bs4 import BeautifulSoup
import re, time, os

SLEEP_TIME_S = 10

def get_page(url,timeout):
	while(True):
		try:
			return urlreq.urlopen(url)
			break
		except urlerr.HTTPError:
			time.sleep(timeout)
			trycount += 1
		print("try " + str(trycount))

def get_poems(url):
    poems = []
	trycount = 0
    page = get_page(url,SLEEP_TIME_S)
    soup = BeautifulSoup(page,"html.parser")
    kona_div = soup.find_all("div",class_ = "KonaBody")
    if kona_div:
        poem = kona_div[0].find('p').text
    
