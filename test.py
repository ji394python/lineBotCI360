import requests 
from bs4 import BeautifulSoup
import lxml

r = requests.get('https://www.ptt.cc/bbs/Stock/index.html')
r = BeautifulSoup(r.text)
r.select('.title')[0].text.strip()
