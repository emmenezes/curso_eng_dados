from logging import Formatter, Logger
import requests
import json
import backoff
import random

# url = 'https://economia.awesomeapi.com.br/last/USD-BRL'
# ret = requests.get(url)

# if ret:
#     print(ret.text)
# else:
#     print('Falhou')

# dolar = json.loads(ret.text)['USDBRL']

# bid = float(dolar['bid'])

def error_check(func):
    def inner_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            print(f"{func.__name__} falhou")
    return inner_func

@error_check
def multi_moeda(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/last/{moeda}'
    ret = requests.get(url)

    cot = json.loads(ret.text)[moeda.replace('-','')]
    print(f"{valor} {moeda[:3]} hoje custam {float(cot['bid']) * valor} {moeda[3:]}")

lst_money = [
    "USD-BRL",
    "EUR-BRL",
    "BTC-BRL",
    "RPL-BRL",
    "JPY-BRL"
]

for moeda in lst_money:
    multi_moeda(20, moeda)

##############  Teste de Backoff ##############

print('a')

@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries=3)
def test_func(*args, **kwargs):
    rnd = random.random()
    log.debug(f"RND: {rnd}")
    log.info(f"args: {args if args else 'sem args'}")
    log.info(f"kwargs: {kwargs if kwargs else 'sem kwards'}")
    if rnd < .2:
        log.error("Conexão foi finalizada")
        raise ConnectionAbortedError()
    elif rnd < .4:
        log.error("Conexão foi recusada")
        raise ConnectionRefusedError()
    elif rnd < .6: 
        log.error("Tempo de espera excedido")
        raise TimeoutError()
    else:
        return 'OK'

key = {
    1: 'a'
}

import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

test_func()