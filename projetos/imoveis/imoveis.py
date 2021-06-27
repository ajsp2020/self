import pandas as pd
from dataImovies import zapImoveisBrasilia

def atualiza_dados():

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

    df = pd.read_csv('./output/data/zapImoveis.csv')
    df = df.drop(columns=['address_1'])
    df = df.dropna().reset_index(drop=True)

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

    a_renomar = {'value': 'preco',
                 'address_2': 'bairro',
                 'areas': 'area_total',
                 'bedrooms': 'quartos',
                 'spaces': 'vagas',
                 'bathrooms': 'banheiros'}

    df = df.rename(columns=a_renomar)

    print(df)



trata_dados()