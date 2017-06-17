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
    for br in soup.find_all("br"):
        br.replace_with("\n")
    solSiir = soup.find("div",{"id":"solSiirMetinDV"})
    title = ""
    if solSiir:
        title = solSiir.find("h1").text.split('-')[0]
    kona_div = soup.find("div",class_ = "KonaBody")
    text = ""
    if kona_div:
        text = kona_div.find('p').text
    if text and title:
        poems.append({"title":title,"text":text})
        print("success")

    try:
        next_link = soup.find('a',{"id":"next_link"})
        next_url = "http://www.poemhunter.com" + next_link.get("href")
    except AttributeError:
        print("END")
        return poems

    print(next_link.get("title").replace(u"\u2018", "'").replace(u"\u2019", "'"))
    poems += get_poems(next_url)

    return poems

if __name__ == "__main__":
    url = input("url?\n")
    filename = input("filename?\n")
    with open(filename,'a') as f:
        for poem in get_poems(url):
            f.write("__BEGIN__")
            f.write("__TITLE__")
            f.write(poem["title"])
            f.write("__TEXT__\n")
            f.write(poem["text"].strip())
            f.write("__END__")
