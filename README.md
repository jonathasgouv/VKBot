# VKBot
**Version 2.1.0**

VKBot is an utility bot that allows you to automate actions related to groups on the VKontakte social network. The bot interacts directly with the users of the group and responds to their requests.

<p align="center">
  <img src="assets/logo.png" width=300>
</p>

## Table of Contents
* [Getting Started](#getting-started)
* [Requirements](#requirements)
* [Environment](#environment)
* [Installing](#installing)
* [Features](#overview)
* [Built With](#built-with)
* [Author](#author)
* [License](#license)

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Requirements
* [Python ^3.8](https://www.python.org/downloads/)
* [Poetry](https://python-poetry.org/docs/)

## Environment
Rename the `.env.example` file to `.env` and set the environment variables below.

### Token
Put your VK acess key on this variable. In order to use all the features of the bot your acess key must have these permissions:
* Notifications
* Offline
* Groups
* Photos

### User_id
Put the id of your bot profile on this variable. It will be used to upload images to your bot profile. See the [image search](#image-search) functionality

### Album_id
Put the id of the album you want the images to be upload to. Note that your bot must have acess to uploading files to this album

### Trigger and Trigger2
You must fill these variables with the string that appears when your bot is quoted on a topic. If you are not sure just quote one of your bot posts and edit the comment, the string will be displayed there.

This is used to assure that your bot is not being called from outside of a topic, or with a fake name.

See the example bellow.
```env
trigger = '[id604740566|Cartola Bot]'
trigger2 = '[id604740566|@cartolabot]'
```
### Message
What ever you put here will be send to the users when your bot is quoted. See the [auto-quote](#auto-quote) functionalty

### Firebase variables
The remaining variables are all used to initialize and configure your firebase databse. Depending on your configuration not all variables are needed. 

## Installing
Run the following commands and you will end up with a local running version of the bot.
```bash
$ git clone https://github.com/jonathasgouv/VKBot.git
$ cd VKBot/
$ poetry install
$ poetry run python main.py
```
And that's it, your VKBot is running.

## Features
### Auto-quote
Whenever your bot is quoted it will quote the user back. This is useful so the topic will always appear on the user notifications, so he can find it on the mobile app, where the search of topics is not available.

### Auto-quote with tag
If the user wants to be quoted with a particular message he can do it by using the `!tag` command.
```
@bot !tag hello world
```

### RemindMe
The bot can schedule a quote. This is useful when the user wants to see a topic just after some time has passed. This can be done using the `!remind` command.

These are the possible variations:
* minute or minutes (525600 minutes maximum)
* hour or hours (8760 hours maximum)
* day or days (365 days maximum)

For example:
```
@bot !remind 1 hour
```

### Image Search
The bot can search an image on the web and append it on his quote through the `!img` command.
```
@bot !img github
```

### Video Download
The bot can send download links to both youtube and VK videos through the `!download` command. Note that in both cases the video must be public.
```
@bot !download https://www.youtube.com/watch?v=8HE2msILkCY
@bot !download https://vk.com/video-179189462_456239395
```

### Live Brazilian Soccer Games
The bot cand send the scoreboards of the games of the day of all brazilian soccer divisions. You can do this by using the `ganes` command.
```
@bot !games
@bot !gamesb
@bot !gamesc
@bot !gamesd
```

## Built With
* [VK API](https://vk.com/dev/methods)
* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Firebase](https://firebase.google.com/)
* [Lxml](https://lxml.de/)

## Author
* [Jônathas Gouveia](https://github.com/jonathasgouv/)

## License
This project is licensed under the  GPL-3.0 License - see the [LICENSE](https://github.com/jonathasgouv/VKBot/blob/master/LICENSE) file for details
