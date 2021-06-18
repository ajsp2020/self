from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

import pandas as pd
from bs4 import BeautifulSoup

def site(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

    try:
        req = Request(url, headers=headers)
        response = urlopen(req)
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    except HTTPError as e:
        print(e.status, e.reason)

    except URLError as e:
        print(e.reason)


def dfImoveis():
    url = 'https://www.dfimoveis.com.br/venda/df/todos/imoveis?pagina=1'
    soup = site(url)

    cards = []
    for i in range(50):
        # Obtendo o HTML
        url = 'https://www.dfimoveis.com.br/venda/df/todos/imoveis?pagina=' + str(i + 1)
        soup = site(url)

        anuncios = soup.find('div', {"id": "resultadoDaBuscaDeImoveis"}).findAll('div', class_="property__info")

        for anuncio in anuncios:
            card = {}
            # Endereços
            endereco = anuncio.find('h3').find('a').getText().replace('\r\n', '').replace('\n', '')
            endereco = " ".join(endereco.split())
            card['address'] = endereco

            # Valor
            precos = anuncio.find('h4', {"class": "property__subtitle hide-mobile"}).findAll('span', class_="price")
            i = 0
            valores = []
            for preco in precos:
                valores.append(preco.get_text())

            for i in range(len(valores)):
                try:
                    card['price'] = valores[0]
                    card['price_m2'] = valores[1]
                except:
                    card['price'] = valores[0]

            # Opções
            items = anuncio.find('div', {"class": "property__info-content"}).findAll('li')
            if items[0].get_text() == items[1].get_text():
                del items[0]

            opcoes = []
            for item in items:
                opcoes.append(item.get_text())
            card['options'] = opcoes


            cards.append(card)

    dataset = pd.DataFrame(cards)
    dataset.to_csv('./output/data/dataset_dfImoveis.csv', index=False, encoding='utf-8-sig')
    return dataset


def zapImoveisBrasilia():
    # url = 'https://www.zapimoveis.com.br/venda/imoveis/df+brasilia/?pagina=1'
    # soup = site(url)
    pages = 100

    cards = []
    for i in range(pages):
        url = 'https://www.zapimoveis.com.br/venda/imoveis/df+brasilia/?pagina=' + str(i + 1)
        soup = site(url)
        anuncios = soup.find('div', {"class": "listings__container"}).findAll('div', class_="card-listing simple-card js-listing-card")

        for anuncio in anuncios:
            card = {}
            # Valor
            value = anuncio.find('p', {"class": "simple-card__price js-price heading-regular heading-regular__bolder align-left"}).getText()
            value = " ".join(value.split())
            card['value'] = value

            # Endereço
            address = anuncio.find('p', {"class": "color-dark text-regular simple-card__address"}).getText()
            address = " ".join(address.split())
            card['address'] = address

            # feature
            items = anuncio.find('div', {"class": "simple-card__actions"}).ul.findAll('li')

            for item in items:
                feature = item.get_text()
                feature = " ".join(feature.split())
                card[item.get('class')[2].split('-')[-1]] = feature

            cards.append(card)

    dataset = pd.DataFrame(cards)
    dataset.to_csv('./output/data/zapImoveis.csv', index=False, encoding='utf-8-sig')
    return dataset





print(zapImoveisBrasilia())