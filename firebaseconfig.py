# -*- coding: utf-8 -*-

from firebase import Firebase
import os

config = {
    "apiKey":os.environ.get('apiKey'),
    "authDomain": os.environ.get('authDomain'),
    "databaseURL": os.environ.get('databaseURL'),
    "storageBucket": os.environ.get('storageBucket')
}

firebase = Firebase(config)
db = firebase.database()
db_child = os.environ.get('db_child') || 'VKBot'
 
def getSchedule():
    return db.child(db_child).child("schedule").get()

def getBanned():
    return db.child(db_child).child("banned").get().val()

def removeFromSchedule(event):
    db.child(db_child).child("schedule").child(event).remove()

def writeToFirebase(cmm, topic, user, comment, time):
    data = {
        'Community': cmm,
        'Topic': topic,
        'User': user,
        'Comment': comment,
        'Time': time
    }

    db.child(db_child).child("schedule").push(data)

def writeToFirebaseBanned(user):
    data = {
        'Uid': user
    }

    db.child(db_child).child("banned").push(data)