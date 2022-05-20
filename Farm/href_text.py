import urllib.request

from bs4 import BeautifulSoup

def get_link(page):  # 寻找链接的href
    linkData = []
    for page in page.find_all('td'):
        links = page.select("a")
        for each in links:
            # if str(each.get('href'))[:1] == '/': 过滤if代码
                data=each.get('href')
                linkData.append(data)
    return(linkData)

url='http://www.nco.ncep.noaa.gov/pmb/codes/nwprod/nosofs.v3.0.4/'
page = urllib.request.urlopen(url).read()
soup = BeautifulSoup(page,'lxml') #利用BeautifulSoup取得网页代码
links=get_link(soup)
# print(links)
for childLink in links:
    #print(childLink )
    links2=url+childLink
    print(links2 )