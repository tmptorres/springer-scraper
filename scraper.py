#!/usr/bin/env python

# System
import time
from random import random
# Data
import re
import pandas as pd
from unicodedata import normalize
# Web
import requests
from bs4 import BeautifulSoup
from wget import download

# Functions
def bar_custom(current, total, width=80):
    print("Downloading: %d%% [%d / %d] MB" % (current / total * 100, current//(2**20), total//(2**20)))
    
# Main Code
pdData = pd.read_excel("Free+English+textbooks.xlsx")

for index, row in pdData.iterrows():
    print("Iteration number {}".format(index))
    
    page = requests.get(row['OpenURL'])
    
    soup = BeautifulSoup(page.content, 'html.parser')
    bookFilename = soup.find(class_="page-title").find("h1").text
    
    for i, auth in enumerate(soup.find_all(class_="authors__name")):
        if i == 0:
            bookFilename = bookFilename + " - " + normalize('NFKD', auth.text)
        else:
            bookFilename = bookFilename + ", " + normalize('NFKD', auth.text)
    
    bookFilename = bookFilename + " - ISBN " + re.search(r"(isbn=([^\n]+))", row['OpenURL']).group(2)
    #print(bookFilename)

    if soup.find(class_="test-bookpdf-link"):
        download("http://link.springer.com" + soup.find(class_="test-bookpdf-link").attrs['href'],
                 "./books/"+bookFilename+".pdf", bar_custom)
        time.sleep(1 + 4*random())
        
    if soup.find(class_="test-bookepub-link"):
        download("http://link.springer.com" + soup.find(class_="test-bookepub-link").attrs['href'],
                 "./books/"+bookFilename+".epub", bar_custom)
        time.sleep(1 + 4*random())
