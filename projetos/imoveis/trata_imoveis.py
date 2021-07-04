import pandas as pd
import seaborn as sns
from dataImovies import zapImoveisBrasilia

def atualiza_dados():
    """ Busca os dados do arquivo csv de acordo com o tamanho dos dados que desejo """

    atualiza = input("Deseja atualizar a base de dados? ").capitalize()

    if atualiza == 'S':
        pages = int(input("Quantas paginas deseja? "))

        if pages < 4:
            zapImoveisBrasilia(4)
        else:
            zapImoveisBrasilia(pages)

        print("Busca de dados concluída!")

    elif atualiza_dados == 'N':
        pass

    else:
        raise ValueError("Valor de entrada incorreto!")


def trata_dados():
    """TRATA OS DADOS DO DATAFRAME E RETORNA UM NOVO DF"""

    df = pd.read_csv('./output/data/zapImoveis.csv')

    ''' iterando sobre a coluna 'address_2' e se seu valor == 'Brasília substituo pelo valor da coluna 'address_1' '''
    for index, row in df.iterrows():

        if str(row['address_2']).lstrip() == 'Brasília':
            df.loc[index, 'address_2'] = str(row['address_1']).lstrip()

        else:
            df.loc[index, 'address_2'] = str(row['address_2']).lstrip()

    df = df.drop(columns=['address_1'])
    df = df.dropna().reset_index(drop=True)

    ''' Iterando sobre o df e trocando o tipo de cada elemento por coluna '''
    for i in range(len(df)):
        try:
            df.loc[i, "value"] = float(df.loc[i, "value"].replace('.', ''))
            try:
                df.loc[i, "areas", "bedrooms", "spaces", "bathrooms"] = int(df.loc[i, "areas", "bedrooms", "spaces",
                                                                                   "bathrooms"])
            except:
                df.loc[i, "areas"] = int(df.loc[i, "areas"].split(sep=" ")[0])
                df.loc[i, "bedrooms"] = int(df.loc[i, "bedrooms"].split(sep=" ")[0])
                df.loc[i, "spaces"] = int(df.loc[i, "spaces"].split(sep=" ")[0])
                df.loc[i, "bathrooms"] = int(df.loc[i, "bathrooms"].split(sep=" ")[0])
        except:
            df = df.drop(labels=i, axis=0)

    df['m2'] = (df.value / df.areas).apply(lambda x: round(x))

    ''' Trocando os nomes das colunas '''
    a_renomar = {'value': 'Valor',
                 'address_2': 'Bairro',
                 'areas': 'Area',
                 'bedrooms': 'Quartos',
                 'spaces': 'Vagas',
                 'bathrooms': 'Banheiros'}

    df = df.rename(columns=a_renomar)

    df.to_csv('./output/data/zap_imoveis_tratado.csv', index=False, encoding='utf-8-sig')
    return df

def classifica_dados():

    df = trata_dados()




classifica_dados()

