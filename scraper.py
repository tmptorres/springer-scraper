#!/usr/bin/env python

# System
import os
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

pdData = pdData.loc[259:]


# Create directory to save books
if not os.path.exists('books'):
    os.mkdir('books')

for index, row in pdData.iterrows():
    print("Iteration number {}".format(index))

    print("Fetching URL: " + row['OpenURL'])
    page = requests.get(row['OpenURL'])
    
    soup = BeautifulSoup(page.content, 'html.parser')
    bookFilename = soup.find(class_="page-title").find("h1").text
    
    for i, auth in enumerate(soup.find_all(class_="authors__name")):
        if i == 0:
            bookFilename = bookFilename + " - " + normalize('NFKD', auth.text)
        else:
            bookFilename = bookFilename + ", " + normalize('NFKD', auth.text)
    
    bookFilename = bookFilename + " - ISBN " + re.search(r"(isbn=([^\n]+))", row['OpenURL']).group(2)
    bookFilename = bookFilename.replace(":", " -").replace("/", ", ").replace("\\", ", ")
    print(bookFilename)

    if soup.find(class_="test-bookpdf-link"):
        link = "http://link.springer.com" + soup.find(class_="test-bookpdf-link").attrs['href']
        print("Downloading: " + link)
        try:
            download(link, "./books/"+bookFilename+".pdf", bar_custom)
        except:
            print("Failed to download: " +  link)
        time.sleep(15*random())
        
    if soup.find(class_="test-bookepub-link"):
        link = "http://link.springer.com" + soup.find(class_="test-bookepub-link").attrs['href']
        print("Downloading: " + link)
        try:
            download(link, "./books/"+bookFilename+".epub", bar_custom)
        except:
            print("Failed to download: " +  link)
        time.sleep(15*random())
