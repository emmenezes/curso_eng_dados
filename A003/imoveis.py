import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import json

url = 'https://www.vivareal.com.br/aluguel/distrito-federal/brasilia/bairros/setor-sudoeste/apartamento_residencial/?pagina={}'

df = pd.DataFrame(
    columns=['Descrição', 'Endereço', 'Área', 'Quartos', 'Banheiros', 'Vagas', 'Valor', 'Condomínio', 'Link']
)

i = 1
ret = requests.get(url.format(i))
soup = bs(ret.text)

houses = soup.find_all('a', {'class': 'property-card__content-link js-card-title'})
qtd_houses = int(soup.find('strong', {'class': 'results-summary__count'}).text.replace('.', ''))


while df.shape[0] < qtd_houses:
    ret = requests.get(url.format(i))
    soup = bs(ret.text)

    houses = soup.find_all('a', {'class': 'property-card__content-link js-card-title'})
    i += 1

    print(url.format(i))
    for house in houses:
        try:
            descricao = house.find('span', {'class': 'property-card__title'}).text.strip() or None
        except:
            descricao = None
        try:
            endereco = house.find('span', {'class': 'property-card__address'}).text.strip()
        except:
            endereco = None
        try:
            area = house.find('span', {'class': 'property-card__detail-area'}).text.strip()
        except:
            area = None
        try:
            quartos = house.find('li', {'class': 'js-property-detail-rooms'}).span.text.strip()
        except:
            quartos = None
        try:
            banheiros = house.find('li', {'class': 'js-property-detail-bathroom'}).span.text.strip()
        except:
            banheiros = None
        try:
            vagas = house.find('li', {'class': 'js-property-detail-garages'}).span.text.strip()
        except:
            vagas = None
        try:
            valor = house.find('div', {'class': 'property-card__price'}).p.text.strip()
        except:
            valor = None
        try:
            condominio = house.find('strong', {'class': 'js-condo-price'}).text.strip()
        except:
            condominio = None
        try:
            hlink = 'https://www.vivareal.com.br' + house['href']
        except:
            hlink = None

        df.loc[df.shape[0]] = [
            descricao, endereco, area, quartos, banheiros, vagas, valor, condominio, hlink
        ]

df.to_csv('imoveis.csv', sep=';', index=False)