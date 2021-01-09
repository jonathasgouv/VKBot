# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as soup
import os
import requests
import json
import urllib
from urllib.request import urlopen as uReq
import urllib.parse
import uuid

access_token = os.environ.get('Token')

def get_soup(url, header):
    return soup(uReq(
        urllib.request.Request(url, headers=header)),
        'html.parser')


def bing_image_search(query):
    query = query.split()
    query = '+'.join(query)
    url = "http://www.bing.com/images/search?q=" + query + "&FORM=HDRSC2"

    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = get_soup(url, header)
    image_result_raw = soup.find("a", {"class": "iusc"})

    m = json.loads(image_result_raw["m"])
    murl, turl = m["murl"], m["turl"]  # mobile image, desktop image

    return (murl)

def getPicture(query):
    query = urllib.parse.quote(query)
    yourUrl = "https://duckduckgo.com/?q=" + query + "&t=h_&iax=images&ia=images"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(yourUrl, headers=headers)
    page = uReq(req)
    img = str(page.read())
    links = img.split('"')
    img = ''

    try:
        img = bing_image_search(query)
    except Exception as e:
        print(e)
        for link in links:
            if ("jpg" in link) or ("jpeg" in link):
                img = link
                break

        if img == '':
            for link in links:
                if (".png" in link) and ("assets" in link) == False:
                    img = link
                    break
        if img == '':
            for link in links:
                if ("https://external-content.duckduckgo.com/" in link):
                    img = link
                    break

    return img


def uploadImage(url):
    data = requests.get(url).content

    img = {'photo': ('img{}.jpg'.format(uuid.uuid1()), data)}

    method_url = 'https://api.vk.com/method/photos.getUploadServer?album_id={}&access_token={}&v=5.52'.format(os.environ.get('album_id'),access_token)
    response = requests.get(method_url)
    result = json.loads(response.text)
    upload_url = result['response']['upload_url']

    response = requests.post(upload_url, files=img)
    result = json.loads(response.text)

    method_url = 'https://api.vk.com/method/photos.save?&album_id={}&server={}&photos_list={}&hash={}&access_token={}&v=5.52'.format(
        os.environ.get('album_id'), result['server'], result['photos_list'], result['hash'], access_token)
    response = requests.get(method_url)
    result = json.loads(response.text)['response'][0]['id']

    return result
