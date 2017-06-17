import urllib.request as urlreq
import urllib.error as urlerr
from bs4 import BeautifulSoup
import re, time, os

SLEEP_TIME_S = 10

def get_poems(url):
    poems = []
	trycount = 0
	while(True):
		try:
			page = urlreq.urlopen(url)
			break
		except urlerr.HTTPError:
			time.sleep(SLEEP_TIME_S)
			trycount += 1
		print("try " + str(trycount))
