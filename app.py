import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbjungle

@app.route('/')
def home():
   return render_template('index.html')


@app.route('/api/list', methods=['GET'])
def show_books():
    result = list(db.bookshop.find({},{'_id':0}).sort('like', -1))
    return jsonify({'result':'success','book_list':result})


@app.route('/api/list', methods=['POST'])
def post_book():
    url_receive = request.form['url_give']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    target = soup.select_one('#yDetailTopWrap > div.topColLft > div.gd_imgArea > span > em > img')

    img_url = target['src']
    title = target['alt']
    author = soup.select_one('span.gd_auth > a:nth-child(1)')
    desc = soup.select_one('div.infoWrap_txtInner > textarea > b')
    rate = soup.select_one('#spanGdRating > a > em')

    if (desc == None) or (rate == None):
        return jsonify({'result': 'success', 'msg':'이 책은 추가할 수 없어요ㅠㅠ'})

    book = {
        'url': url_receive,
        'title': title,
        'img': img_url,
        'author': author.text,
        'desc': desc.text,
        'rate': rate.text,
        'like': 0,
    }

    db.bookshop.insert_one(book)
    return jsonify({'result': 'success', 'msg':'추가 완료!'})


@app.route('/api/like', methods=['POST'])
def like_book():
    book_receive = request.form['book_give']
    book = db.bookshop.find_one({'title':book_receive},{'_id':0})
    new_like = book['like'] + 1
    db.bookshop.update_one({'title':book_receive}, {'$set':{'like':new_like}})
    return jsonify({'result': 'success', 'msg': '위로!'})


@app.route('/api/dislike', methods=['POST'])
def dislike_book():
    book_receive = request.form['book_give']
    book = db.bookshop.find_one({'title': book_receive}, {'_id': 0})
    new_like = book['like'] - 1
    db.bookshop.update_one({'title': book_receive}, {'$set': {'like': new_like}})
    return jsonify({'result': 'success', 'msg': '아래로!'})


if __name__ == '__main__':
   app.run()