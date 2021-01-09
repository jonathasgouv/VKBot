# -*- coding: utf-8 -*-

import requests
from lxml import etree
import urllib
from urllib.request import urlopen
import json
import uuid
from youtube_dl import YoutubeDL

def getYoutubeUrl(url):
    ydl = YoutubeDL()
    r = ydl.extract_info(url, download=False)
    # if any link will do
    #urls = [format['url'] for format in r['formats']]

    # if you want links with video and audio
    urls = [f['url'] for f in r['formats'] if f['acodec'] != 'none' and f['vcodec'] != 'none']

    file_name = '{}.mp4'.format(uuid.uuid1())
    rsp = urlopen(urls[0])
    files = {
        'file': (file_name, rsp.read()),
    }

    response = requests.post('https://api.anonymousfiles.io/', files=files)

    return response.json()['url']


def downloadVideo(data):
    list = data[0]
    condition = data[1]

    if condition == True:
        for key in list:
            print('chegui aquiii')
            if 'mp4_240' in str(key):
                file_name = '{}.mp4'.format(uuid.uuid1())
                rsp = urlopen(list[key])
                files = {
                    'file': (file_name, rsp.read()),
                }

                response = requests.post('https://api.anonymousfiles.io/', files=files)

                return response.json()['url']

            elif 'mp4_360' in str(key):
                file_name = '{}.mp4'.format(uuid.uuid1())
                rsp = urlopen(list[key])
                files = {
                    'file': (file_name, rsp.read()),
                }

                response = requests.post('https://api.anonymousfiles.io/', files=files)

                return response.json()['url']
    elif condition == False:
        for link in list:
            if '.240' in str(link):
                file_name = '{}.mp4'.format(uuid.uuid1())
                rsp = urlopen(link)
                files = {
                    'file': (file_name, rsp.read()),
                }

                response = requests.post('https://api.anonymousfiles.io/', files=files)

                return response.json()['url']

            if '.360' in str(link):
                file_name = '{}.mp4'.format(uuid.uuid1())
                rsp = urlopen(link)
                files = {
                    'file': (file_name, rsp.read()),
                }

                response = requests.post('https://api.anonymousfiles.io/', files=files)

                return response.json()['url']

            if '.480' in str(link):
                file_name = '{}.mp4'.format(uuid.uuid1())
                rsp = urlopen(link)
                files = {
                    'file': (file_name, rsp.read()),
                }

                response = requests.post('https://api.anonymousfiles.io/', files=files)

                return response.json()['url']


def filterLinks(link):
    if '.mp4' in str(link):
        return True
    else:
        return False


def getVideo(id):
    try:
        print(id)
        yourUrl = "https://savevk.com/video{}".format(id)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = urllib.request.Request(yourUrl, headers=headers)
        page = urlopen(req)
        htmlparser = etree.HTMLParser()
        treegoogle = etree.parse(page, htmlparser)

        jsondata = \
        str(treegoogle.xpath('/html/body/script[1]/text()')[0]).split('window.videoParams = ')[1].replace("\n",
                                                                                                          "").replace(
            " ", "").split(';')[0].replace("id", '"id"').replace("server", '"server"').replace("credentials",
                                                                                               '"credentials"').replace(
            "token", '"token"').replace(
            "c_key", '"c_key"').replace("q_key", '"q_key"').replace("e_key", '"e_key"').replace('i_key', '"i_key"')
        print(jsondata)

        finaljson = json.loads(jsondata)

        url = 'https://psv78-3.daxab.com/method/video.get?credentials={}&token={}&videos={}&extra_key={}&ckey={}'.format(
            finaljson['credentials'], finaljson['token'], finaljson['id'], finaljson['e_key'], finaljson['c_key'])

        print(url)

        response = requests.get(url)
        video = response.json()['response']['items'][0]['files']
        extrakeys = finaljson['q_key']

        for key in video:
            for exk in extrakeys:
                print('{} - {}'.format(exk, key))
                if str(exk) in str(key):
                    print('cheeguei')
                    video[key] += '&extra_key={}&videos={}&dl=1'.format(extrakeys[exk], finaljson['id'])
                    video[key] = video[key].split('https://')[1]
                    video[key] = 'https://psv78-3.daxab.com/' + video[key]

                    if key == 'hls' or key == 'hls_raw':
                        video.pop(key)

        print(video)
        if len(video) > 1:
            return (video, True)
        else:
            raise Exception('entrando no scraping')
    except:
        print('entrei na exceção')
        idowner = id.split('_')[0]
        responsevideo = requests.get(
            'https://api.vk.com/method/video.get?owner_id={}&videos={}&access_token={}&v=5.122'.format(
                idowner, id, access_token))

        videoplayer = responsevideo.json()['response']['items'][0]['player']

        print("[+]" + " Video: " + videoplayer)
        page = urlopen(videoplayer)
        content = page.read()
        print(content)
        page.close()
        links = str(content).split('"')
        finallinks = []

        for link in links:
            if '.mp4' in link:
                finallinks.append(link)

        if len(finallinks) == 0:
            return
        else:
            return (finallinks, False)