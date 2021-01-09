# -*- coding: utf-8 -*-

import firebaseconfig, image, video, games
import urllib
import urllib.parse
import requests
import time
from datetime import datetime
import os

limitecitadas = 0

users = []
replyed = []
start_time = 0
trigger = os.environ.get('trigger_1')
trigger2 = os.environ.get('trigger_2')

access_token = os.environ.get('Token')
messagetext = os.environ.get('message') || 'did you call me?'


def replyimg(cmm, topic, user, comment, message):
    global users, limitecitadas

    users.append(user)
    if limitecitadas > 5:
        print('limite atingido')
        return

    # Put the words you want the bot to ignore here
    blacklist = ['piroca', 'penis', 'anal', 'prolapso anal', 'sexo', 'shemale', 'traveco', 'travesti', 'pênis',
                 'melhor do mundo', 'rola', 'tripofobia', 'calcanhar de maracujá', 'calcanhar de maracuja',
                 'bilola' 'calcanhar maracuja', 'calcanhar', 'calcanar', 'maracuja', 'maracuja', 'bilola', 'pauzao',
                 'cintaralho', 'pau', 'genital', 'fuck', 'selfsuck', 'suck', 'cruzando', 'naked', 'cuceta', 'gangbang',
                 'two girls one cup', '2 girls 1 cup', 'nipple', 'gay', 'xere']

    query = message.split('!img')[1].strip()
    # query = unidecode.unidecode(query).lower()

    for word in blacklist:
        if word in query:
            return

    request = requests.get('https://api.vk.com/method/users.get?user_ids={}&access_token={}&v=5.52'.format(user, access_token))
    name = request.json()['response'][0]['first_name']

    print('cheguei aqui')
    print(query)
    try:
        attachment = 'photo{}_{}'.format(os.environ.get('user_id'), image.uploadImage(image.getPicture(query)))
    except Exception as e:
        print('attachment error')
        print(e)
        return

    message = '[post{}|{}], here is your image'.format(comment, name)

    url = 'https://api.vk.com/method/board.createComment?group_id={}&topic_id={}&message={}&attachments={}&access_token={}&v=5.52'.format(str(cmm).split('-')[1], topic, str(message), attachment, access_token)
    requests.get(url)

    limitecitadas += 1

def replyComandos(cmm, topic, user, comment):
    global users

    users.append(user)

    request = requests.get(
        'https://api.vk.com/method/users.get?user_ids={}&access_token={}&v=5.52'.format(user, access_token))
    name = request.json()['response'][0]['first_name']

    comandos = 'take a look at my profile'

    comandos = urllib.parse.quote(comandos)

    message = '[post{}|{}],  {}'.format(comment, name, comandos)

    url = 'https://api.vk.com/method/board.createComment?group_id={}&topic_id={}&message={}&access_token={}&v=5.52'.format(
        str(cmm).split('-')[1], topic, str(message), access_token)
    requests.get(url)



def replyJogos(cmm, topic, user, comment, serie):
    global users
    serie = serie.upper()
    users.append(user)
    request = requests.get(
        'https://api.vk.com/method/users.get?user_ids={}&access_token={}&v=5.52'.format(user, access_token))
    name = request.json()['response'][0]['first_name']

    jogos = games.getLiveScore(serie)

    if len(jogos) == 0:
        message = '[post{}|{}], there is no Brazilian Serie {} games today :('.format(comment, name, serie)

        url = 'https://api.vk.com/method/board.createComment?group_id={}&topic_id={}&message={}&access_token={}&v=5.52'.format(
            str(cmm).split('-')[1], topic, str(message), access_token)
        requests.get(url)
        return

    textofinal = ''

    for jogo in jogos:
        textofinal += jogo['condition'] + ' - ' + jogo['horario'] + ' - ' + jogo['estado'] + '\n'

    jogosdehoje = urllib.parse.quote(textofinal)

    message = '[post{}|{}], these are the today games: \n {}'.format(comment, name, jogosdehoje)

    url = 'https://api.vk.com/method/board.createComment?group_id={}&topic_id={}&message={}&access_token={}&v=5.52'.format(str(cmm).split('-')[1], topic, message, access_token)
    requests.get(url)



def replyVideo(cmm, topic, user, comment, linkmessage):
    request = requests.get('https://api.vk.com/method/users.get?user_ids={}&access_token={}&v=5.52'.format(user, access_token))
    name = request.json()['response'][0]['first_name'].encode('utf-8')

    if 'youtube' in linkmessage:
        id = linkmessage.split('https://www.youtube.com/watch?v=')[1]
        videolink = 'https://www.youtube.com/watch?v=' + id
        link = video.getYoutubeUrl(videolink)

        message = '[post{}|{}], try this: \n{}'.format(comment, name, link)

        url = 'https://api.vk.com/method/board.createComment?group_id={}&topic_id={}&message={}&access_token={}&v=5.52'.format(str(cmm).split('-')[1], topic, str(message), access_token)
        requests.get(url)
        return

    id = linkmessage.split('https://vk.com/video')[1]
    linkslist = video.downloadVideo(video.getVideo(id))

    message = '[post{}|{}], try this: \n{}'.format(comment, name, linkslist)

    url = 'https://api.vk.com/method/board.createComment?group_id={}&topic_id={}&message={}&access_token={}&v=5.52'.format(str(cmm).split('-')[1], topic, str(message), access_token)
    requests.get(url)


def remindMe():
    schedule = firebaseconfig.getSchedule()

    if schedule == None:
        return

    for reminder in schedule.each():
        event = reminder.val()
        print(event)
        currentTime = int(time.mktime(datetime.now().timetuple()))
        if int(event['Time']) < currentTime:
            reply(event['Community'], event['Topic'], event['User'], event['Comment'])
            firebaseconfig.removeFromSchedule(reminder.key())


def getNotifications():
    global replyed
    global users

    bannedlist = firebaseconfig.getBanned()

    # Put an user id here to mannualy ban him. Any user with his id on this array will be ignored by the bot
    banned = []

    if bannedlist != None:
        for userbanned in bannedlist:
            banned.append(userbanned)

    request = requests.get('https://api.vk.com/method/notifications.get?filters=mentions&count=5&start_time={}&access_token={}&v=5.52'.format(start_time, access_token))
    notifications = request.json()['response']['items']
    for notification in notifications:
        if str(notification['type']) == 'reply_topic':
            cmm = notification['parent']['owner_id']
            topic = notification['parent']['id']
            user = notification['feedback']['from_id']
            comment = notification['feedback']['id']
            title = notification['parent']['title']
            message = notification['feedback']['text']

            date = int(time.mktime(datetime.now().timetuple()))

            if str(user) in banned:
                continue

            if comment not in replyed and (trigger in str(message) or trigger2 in str(message)):
                replyed.append(comment)
                try:
                    if '!remind' in str(message):
                        if trigger in message:
                            remindertime = message.split(trigger + ' !remind')[1].split(' ')[1]
                            remindermagnitude = message.split(trigger + ' !remind')[1].split(' ')[2]
                        elif trigger2 in message:
                            remindertime = message.split(trigger2 + ' !remind')[1].split(' ')[1]
                            remindermagnitude = message.split(trigger2 + ' !remind')[1].split(' ')[2]

                        if (str(remindermagnitude) == 'hours') or (str(remindermagnitude) == 'hour'):
                            if int(remindertime) <= 365 * 24:
                                firebaseconfig.writeToFirebase(cmm, topic, user, comment, (date + int(remindertime) * 3600))
                        elif (str(remindermagnitude) == 'minutes') or (str(remindermagnitude) == 'minute'):
                            if int(remindertime) <= 365 * 24 * 60:
                                firebaseconfig.writeToFirebase(cmm, topic, user, comment, (date + int(remindertime) * 60))
                        elif (str(remindermagnitude) == 'days') or (str(remindermagnitude) == 'day'):
                            if int(remindertime) <= 365:
                                firebaseconfig.writeToFirebase(cmm, topic, user, comment,(int(date) + int(remindertime) * 3600 * 24))
                    elif '!img' in str(message):
                        replyimg(cmm, topic, user, comment, message)
                    elif '!tag' in str(message):
                        reply(cmm, topic, user, comment, message, True)
                    elif '!download' in str(message):
                        # This can take too much time and make the bot lose some notifications, consider running it on a separate environment
                        replyVideo(cmm, topic, user, comment, message)
                    elif '!gamessd' in str(message):
                        replyJogos(cmm, topic, user, comment, 'D')
                    elif '!gamesc' in str(message):
                        replyJogos(cmm, topic, user, comment, 'C')
                    elif '!gamesb' in str(message):
                        replyJogos(cmm, topic, user, comment, 'B')
                    elif '!games' in str(message):
                        replyJogos(cmm, topic, user, comment, 'A')
                    elif '!comandos' in str(message):
                        replyComandos(cmm, topic, user, comment)
                    elif '!' in str(message):
                        return
                    else:
                        reply(cmm, topic, user, comment)
                except Exception as e:
                    print(e)
                    pass


def reply(cmm, topic, user, comment, commenttext='', tag=False):
    global users, messagetext
    users.append(user)
    request = requests.get(
        'https://api.vk.com/method/users.get?user_ids={}&access_token={}&v=5.52'.format(user, access_token))
    name = request.json()['response'][0]['first_name']
    if tag == False:
        message = '[post{}|{}], {}'.format(comment, name, messagetext)
    else:
        tag = commenttext.split('!tag')[1].strip()
        message = '[post{}|{}], {}'.format(comment, name, tag)
    url = 'https://api.vk.com/method/board.createComment?group_id={}&topic_id={}&message={}&access_token={}&v=5.52'.format(
        str(cmm).split('-')[1], topic, str(message), access_token)
    requests.get(url)


def acceptInvites():
    request = requests.get('https://api.vk.com/method/groups.getInvites?count=100&offset=0&access_token={}&v=5.52'.format(access_token))
    invites = request.json()['response']['items']
    for invite in invites:
        if invite['type'] == 'group':
            id = invite['id']
            requests.get(
                'https://api.vk.com/method/groups.join?group_id={}&access_token={}&v=5.52'.format(id, access_token))


def run():
    try:
        global replyed
        global start_time
        global limitecitadas
        global users
        start_time = int(time.mktime(datetime.now().timetuple()) - 2)
        while True:
            time.sleep(1)
            getNotifications()
            minutes = int(datetime.now().minute)
            seconds = float(datetime.now().second)
            if minutes in [0, 10, 20, 30, 40, 50] and float(seconds) < 2:
                for user in list(set(users)):
                    if users.count(user) > 6:
                        firebaseconfig.writeToFirebaseBanned(user)
                limitecitadas = 0
                users = []
            if float(seconds) < 2:
                remindMe()
            if minutes == 0 and float(seconds) < 2 or minutes == 30 and float(seconds) < 2:
                acceptInvites()
            if len(replyed) > 10:
                replyed = replyed[-10:]
    except Exception as e:
        print(e)
        time.sleep(2)
        run()