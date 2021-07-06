from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import pandas as pd

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

def regioes_df(url, regiao):


    soup = site(url)

    lista_cidades = []
    for card in soup.findAll('div', {"class": "filter-card"}):

        cidades = (card.findAll('a', {"class": "filter-card__link gtm-filtro-de-"+str(regiao)+" to-upper"}))

        for cidade in cidades:
            cidade = cidade.find('div', {"itemprop":"name"})
            lista_cidades.append(cidade.get_text())


    return lista_cidades

def imovel(page, cidade, bairro=''):

    cards = []
    for i in range(page):

        if cidade == 'brasilia':
            url = 'https://www.dfimoveis.com.br/venda/df/brasilia/' + bairro + '/imoveis?pagina=' + str(i + 1)

        else:
            url = 'https://www.dfimoveis.com.br/venda/df/' + cidade + '/imoveis?pagina=' + str(i + 1)

        soup = site(url)
        anuncios = soup.findAll('div', {"class": "property__info-content"})

        for anuncio in anuncios:
            card = {}
            # região
            card['Cidade'] = cidade
            card['Bairro'] = bairro

            # Valor
            preco = anuncio.find('h4', {"class": "property__subtitle hide-mobile"}).find('span',
                                                                                         class_="price").get_text()

            try:
                preco = preco.replace('.', '')
                card['Preco'] = float(preco)

            except:
                card['Preco'] = ''

                # Opções
            items = anuncio.findAll('li')
            for item in items:
                item = item.get_text().split()

                try:
                    item[-1] = item[-1].capitalize()
                    if item[-1][-1] == 's':
                        item[-1] = item[-1][:-1]
                        if item[-1] == 'M²' or item[-1] == 'Quarto' or item[-1] == 'Vaga' or item[-1] == 'Suíte':
                            card[item[-1]] = item[-2]
                            if item[-3] == 'Condominio':
                                card['Tipo'] = item[-4]
                            else:
                                card['Tipo'] = item[-3]
                    else:

                        if item[-1] == 'M²' or item[-1] == 'Quarto' or item[-1] == 'Vaga' or item[-1] == 'Suíte':
                            card[item[-1]] = item[-2]
                            if item[-3] == 'Condominio':
                                card['Tipo'] = item[-4]
                            else:
                                card['Tipo'] = item[-3]

                except:
                    pass
            cards.append(card)

    return cards

def imoveis_df():

    url = 'https://www.dfimoveis.com.br/venda/df/todos/imoveis?pagina=1'
    regioes = regioes_df(url, 'cidade')
    cidades = list(map(lambda cidade: cidade.lower().replace(' ', '-'), regioes))

    cards = []
    pages = 2
    for cidade in cidades:
        if cidade == 'brasilia':
            url = 'https://www.dfimoveis.com.br/venda/df/brasilia/imoveis'
            regioes = regioes_df(url, 'bairro')
            bairros = list(map(lambda bairro: bairro.lower().replace(' ', '-'), regioes))

            for bairro in bairros:
                card = imovel(pages, cidade, bairro)
                cards.extend(card)
                print(bairro)

        else:
            card = imovel(pages, cidade, cidade)
            cards.extend(card)
            print(cidade)

    dataframe = pd.DataFrame(cards)
    dataframe.to_csv('./output/data/dfImoveis.csv', index=False, encoding='utf-8-sig')
    print(dataframe)


imoveis_df()



