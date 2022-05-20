from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
url = 'http://www.lswz.gov.cn/html/ywpd/lstk/tj-sgsj.shtml'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')
for a in soup.find_all('a'):
    url1 = 'http://www.lswz.gov.cn/html/ywpd/lstk/tj-sgsj.shtml'
    url2 = a['href']
    print(urljoin(url1, url2), url2)

