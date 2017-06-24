from bs4 import BeautifulSoup
import urllib2
import re
from urllib import urlretrieve
import requests
import sys
import subprocess

url = "http://www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Main/8kHz_16bit/"

def downloadpage(url):
    page = urllib2.urlopen(url).read()
    f = open("page.html", "w+")
    f.write(page)
    f.close()

def extractlinks():
    page = open("page.html", "r").read()
    soup = BeautifulSoup(page, 'html.parser')
    usernames = []
    links = []
    for link in soup.findAll('a'):
        value = link.get('href')
        splitlink = value.split(".")
        value = value.split('-')[0] 
        if value not in usernames and splitlink[-1] == "tgz": 
            links.append(str(link.get('href')))
            usernames.append(value)
    return links

def download(links, url):
    for link in links:
        urllib2.urlretrieve(url+link)
        

links = extractlinks()
for link in links:
    urlretrieve(url + link, link)
    subprocess.call("tar -xvzf " + link, shell=True)
    subprocess.call("rm -rf " + link, shell=True)
