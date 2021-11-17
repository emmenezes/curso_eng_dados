import requests
import pandas as pd
import collections
import sys

# url = 'http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbz8vTxNDRy9_Y2NQ13CDA0sTIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wBmoxN_FydLAGAgNTKEK8DkRrACPGwpyQyMMMj0VAcySpRM!/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0K85260Q5OIRSC42046/res/id=historicoHTML/c=cacheLevelPage/=/'
url = sys.argv[1]

r = requests.get(url)

r_text = r.text

df = pd.read_html(r_text)

df = df[0].copy()

nr_pop = list(range(1,26))
nr_pares = [2*x for x in range(1, 13)]
nr_primos = [2, 3, 5, 7, 11, 13, 17, 19, 23]

vezes = [[x, 0] for x in range(26)]
comb = []

lst_campos = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Bola7',
              'Bola8', 'Bola9', 'Bola10', 'Bola11', 'Bola12', 'Bola13', 
              'Bola14', 'Bola15']

for index, row in df.iterrows():
    vezes_pares = 0
    vezes_impares = 0
    vezes_primos = 0
    for campo in lst_campos:
        if row[campo] in nr_pares:
            vezes_pares += 1
        else:
            vezes_impares += 1
        if row[campo] in nr_primos:
            vezes_primos += 1
        vezes[row[campo]][1] += 1
    
    comb.append(f"{vezes_pares}, {vezes_impares}, {vezes_primos}")

vezes = sorted(vezes, key=lambda x: -x[1])

counter = collections.Counter(comb)
resultado = pd.DataFrame(counter.items(), columns=['Combinacao', 'Frequencia'])

resultado['p_freq'] = resultado['Frequencia']/resultado['Frequencia'].sum()
resultado = resultado.sort_values(by='p_freq')

print('''

O número mais frequente: {}
O número menos frequente: {}
A combinação de pares, ímpares e primos mais frequente é: {}, com a frequência de {:.2f}%

'''. format(vezes[0][0], vezes[-1][0], resultado['Combinacao'].values[-1],
            resultado['p_freq'].values[-1]*100))