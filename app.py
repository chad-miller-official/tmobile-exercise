import random
from flask import Flask, jsonify, redirect, request

app = Flask(__name__)

URLS = {}
REVERSE_URLS = {}

URL_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'
URL_LENGTH = 8

random.seed()

def generate_url_uid(url):
    rval = ''

    for i in range(8):
        rval += URL_CHARS[int(random.random() * len(URL_CHARS))]

    return rval

@app.route('/<url_uid>')
def lengthen(url_uid):
    url_obj = REVERSE_URLS.get(url_uid)

    if url_obj:
        url_obj['hits'] += 1
        print(f"{url_obj['hits']}")
        return redirect(url_obj['url'], 302)

    return jsonify({ 'message': 'URL UID does not exist' }), 404

@app.route('/')
def index():
    url = request.args.get('url')

    if URLS.get(url):
        return jsonify({
            'url': f'http://localhost:5000/{URLS[url]}',
            'hits': REVERSE_URLS[URLS[url]]['hits'],
        })

    url_uid = generate_url_uid(url)

    while url_uid in URLS.values():
        url_uid = generate_url_uid(url)

    URLS[url] = url_uid

    REVERSE_URLS[url_uid] = {
        'url': url,
        'hits': 0,
    }

    return jsonify({
        'url': f'http://localhost:5000/{URLS[url]}',
        'hits': 0,
    })
