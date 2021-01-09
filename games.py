# -*- coding: utf-8 -*-

from urllib.request import urlopen as uReq
from lxml import etree

def getLiveScore(serie):
    response = uReq('https://www.cbf.com.br/futebol-brasileiro/placar-ao-vivo')
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    numberOfGamesToday = len(tree.xpath("//div[@class='box p-t-25 p-b-15 m-b-15']"))

    games = []

    for game in range(1, numberOfGamesToday + 1):
        campeonato = tree.xpath('//*[@id="menu-panel"]/article/div/div/div/section/div[{}]/div/div[3]'.format(game))[0].text.split(
            '-')[0].split(' ')[-2]

        if campeonato == serie.upper():
            mandante = tree.xpath('//*[@id="menu-panel"]/article/div/div/div/section/div[{}]/div/div[2]/div[1]/div'.format(game))[0].text
            visitante = tree.xpath('//*[@id="menu-panel"]/article/div/div/div/section/div[{}]/div/div[2]/div[3]/div'.format(game))[0].text
            placar = tree.xpath('//*[@id="menu-panel"]/article/div/div/div/section/div[{}]/div/div[2]/div[2]/div/b'.format(game))[0].text
            estado = tree.xpath('//*[@id="menu-panel"]/article/div/div/div/section/div[{}]/div/div[1]'.format(game))[0].text.split('-')[-1].split(' ')[1]
            horario = tree.xpath('//*[@id="menu-panel"]/article/div/div/div/section/div[{}]/div/div[1]'.format(game))[0].text.split('-')[0].split(' ')[-2]

            estado = estado.strip()

            if estado == 'Em':
                estado = 'In progress'
            elif estado == 'Finished':
                pass
            else:
                placar = 'x'

            condition = mandante.strip() + ' ' + placar.strip() + ' ' + visitante.strip()

            jogo = {"horario":horario.strip(), "estado":estado.strip(), "condition": condition}
            games.append(jogo)

    return games