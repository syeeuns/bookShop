import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbjungle

def get_urls():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    base_url = 'http://www.yes24.com/24/category/bestseller?CategoryNumber=001&sumgb=06&FetchSize=40'
    data = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    target = soup.select('#bestList tr')
    mom_url = 'http://www.yes24.com'
    urls = []

    for one in target:
        book = one.select_one('.goodsTxtInfo a')
        if book:
            url = mom_url + book['href']
            urls.append(url)
    return urls


def insert_book(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    target = soup.select_one('#yDetailTopWrap > div.topColLft > div.gd_imgArea > span > em > img')

    img_url = target['src']
    title = target['alt']
    author = soup.select_one('span.gd_auth > a:nth-child(1)')
    desc = soup.select_one('div.infoWrap_txtInner > textarea > b')
    rate = soup.select_one('#spanGdRating > a > em')

    if (desc == None) or (rate == None):
        return

    book = {
        'url':url,
        'title':title,
        'img':img_url,
        'author':author.text,
        'desc':desc.text,
        'rate':rate.text,
        'like':0,
    }

    db.bookshop.insert_one(book)
    print('완료!', title)


def insert_all():
    db.bookshop.drop()
    urls = get_urls()
    for url in urls:
        insert_book(url)


insert_all()