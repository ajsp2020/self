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

# pensar num modo de automatizar o processo
def imoveis_df(cidade, page):

    cidade = cidade.lower().replace(' ','-')

    if cidade == 'brasilia':
        url = 'https://www.dfimoveis.com.br/venda/df/brasilia/imoveis'
        regioes = regioes_df(url, 'bairro')
        print(regioes)

    else:
        url = 'https://www.dfimoveis.com.br/venda/df/todos/imoveis?pagina=1'
        regioes = regioes_df(url, 'cidade')

    cards = []

    for i in range(page):

        if cidade == 'brasilia':
            bairro = 'noroeste'
            url = 'https://www.dfimoveis.com.br/venda/df/brasilia/'+bairro+'/imoveis?pagina=2'

        else:
            url = 'https://www.dfimoveis.com.br/venda/df/'+cidade+'/imoveis?pagina=' + str(i+1)

        soup = site(url)
        anuncios = soup.findAll('div', {"class": "property__info-content"})

        for anuncio in anuncios:
            card = {}
            # região


            # Valor
            preco = anuncio.find('h4', {"class": "property__subtitle hide-mobile"}).find('span', class_="price").get_text()
            card['Preco'] = preco

            # Opções
            items = anuncio.findAll('li')
            for item in items:
                item = item.get_text().split()
                # item = item.split()
                retira = ['Construção', 'Planta']
                try:
                    item[-1] = item[-1].capitalize()
                    if item[-1][-1] == 's':
                        item[-1] = item[-1][:-1]
                        if item[-1] != 'Construção':
                            if item[-1] != 'Planta':
                                card[item[-1]] = item[-2]
                    else:
                        if item[-1] != 'Construção':
                            if item[-1] != 'Planta':
                                card[item[-1]] = item[-2]

                except:
                    pass

            cards.append(card)


        dataframe = pd.DataFrame(cards)
        dataframe.to_csv('./output/data/dfImoveis.csv', index=False, encoding='utf-8-sig')


# imoveis_df("AGUAS CLARAS", 10)
imoveis_df("BRASILIA", 10)

