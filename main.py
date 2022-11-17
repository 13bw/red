import csv
import time
from flask import Flask, render_template
from flask_socketio import SocketIO
import webbrowser

import requests
from bs4 import BeautifulSoup
app = Flask(__name__)
io = SocketIO(app, async_mode="threading")


def saveData(data, filename):
    with open(filename, "w", encoding="utf8", newline="") as fp:
        write = csv.DictWriter(fp, data[0].keys())
        write.writeheader()
        write.writerows(data)


def alligatorSearch(pesquisa):
    alligatorData = list()

    text = requests.get("https://www.alligatorshop.com.br/produtos?q="+pesquisa).text
    soup = BeautifulSoup(text, "lxml")
    divsAlligator = soup.find_all("div", {"class": "product-card"})

    for div in divsAlligator:
        nomeproduto = div.find("h2", {"class": "text"})
        imgproduto = div.find("img", {"class": "img-fluid"})
        precoproduto = div.find("span", {"class": "price total"})
        
        if imgproduto:
            imgproduto = imgproduto["src"]
        
        if nomeproduto:
            nomeproduto = str(nomeproduto.text).strip()
        
        if precoproduto:
            precoproduto = precoproduto.text

        alligatorData.append(
            {
                "nome": nomeproduto,
                "preco": precoproduto,
                "imagem": imgproduto
            }
        )
    
    saveData(alligatorData, "alligator.csv")
    return alligatorData[0:3]
        


def kalungaSearch(pesquisa):
    kalungaData = list()
    reqKalunga = requests.get('https://www.kalunga.com.br/busca/1?q='+pesquisa)
    soupKalunga = BeautifulSoup(reqKalunga.text, 'lxml')
    divsKalunga = soupKalunga.find_all('div', {'class': 'blocoproduto'})

    for div in divsKalunga:
        nomeproduto = div.find('h2', {'class': 'blocoproduto__title'})
        precoproduto = div.find(
            'div', {'class': 'blocoproduto__box'}).find('span')
        imgproduto = div.find('img', {'class': 'blocoproduto__image'})

        if nomeproduto:
            nomeproduto = nomeproduto.text

        if precoproduto:
            precoproduto = precoproduto.text

        if imgproduto:
            imgproduto = imgproduto['data-src']

        kalungaData.append({
            "nome": nomeproduto,
            "preco": precoproduto,
            "imagem": imgproduto
        })
    saveData(kalungaData, "kalunga.csv")
    return kalungaData[0:3]


def amazonSearch(pesquisa):
    amazonData = list()

    divsAmazon = []
    while not divsAmazon:

        time.sleep(1)
        reqAmazon = requests.get("https://www.amazon.com.br/s?k="+pesquisa)
        soupAmazon = BeautifulSoup(reqAmazon.text, "lxml")
        divsAmazon = soupAmazon.find_all(
            "div", {"class": "a-section a-spacing-micro puis-padding-left-small puis-padding-right-small"})

        for div in divsAmazon:

            nomeproduto = div.find(
                "span", {"class": "a-size-base-plus a-color-base a-text-normal"})
            precoproduto = div.find("span", {"class": "a-offscreen"})

            if nomeproduto:
                nomeproduto = nomeproduto.text

            if precoproduto:
                precoproduto = precoproduto.text

            amazonData.append(
                {
                    "nome": nomeproduto,
                    "preco": precoproduto,
                }
            )

    saveData(amazonData, "amazon.csv")
    return amazonData


@app.route("/")
def home():
    return render_template("index.html")


@io.on("search")
def search(msg):
    io.emit("getQuery",
            {
                "kalunga": kalungaSearch(msg["data"]),
                "alligator": alligatorSearch(msg["data"])
            }
            )
    amazonSearch(msg["data"])


webbrowser.open("http://localhost:5000")
io.run(app)
