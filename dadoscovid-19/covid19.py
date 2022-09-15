from time import strftime
from numpy import append
import requests as requisicao
import datetime as datapaais
import csv
from PIL import Image
from IPython.display import display
from urllib.parse import quote
"""
Informações que desejo obter do api
(Confimado Recuperado Ativos Morte Data)
Constantes para criação do data Grid
(Confirmados Obitos Recuperados Ativos Data )
"""
CONFIRMADOS = 0
OBITOS = 1
RECUPERADOS = 2
ATIVOS = 3
DATA = 4

url = 'https://api.covid19api.com/dayone/country/brazil'
resposta = requisicao.get(url)
teste_conexao = resposta.status_code
if(teste_conexao == 200):
    dados_lidos = resposta.json()
    print("Consumindo Api")
elif(teste_conexao == 404):
    print('Sem conexaõ com o API')

dados_solicitados = []
for informacao_obtida in dados_lidos:
    dados_solicitados.append([informacao_obtida['Confirmed'],informacao_obtida['Deaths'],informacao_obtida['Recovered'],informacao_obtida['Active'],informacao_obtida['Date']])
dados_solicitados.insert(0, ['Confirmados','Obitos','Recuperados','Ativos','Data'])

for i in range(1, len(dados_solicitados)):
    dados_solicitados[i][DATA] = dados_solicitados[i][DATA][:10]
with open('dados-covid-brasil.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(dados_solicitados)
for i in range(1, len(dados_solicitados)):
    dados_solicitados[i][DATA] = datapaais.datetime.strptime(dados_solicitados[i][DATA], '%Y-%m-%d')

def get_montar_grafico(y, labels):
    if type(y[0]) == list:
        dados_grid = []
        for i in range(len(y)):
            dados_grid.append({
                'label':labels[i],
                'data':y[i]
            })
            return dados_grid
    else:
        return [
            {
                'label':labels[0],
                'data':y
             }
        ]    
def set_titulo(title=''):
    if title != '':
        display = 'true'
    else:
        display = 'false'
    return {
        'title':title,
        'display':display
    }        
def create_chart(x, y, labels, kind='bar', title=''):
        dados_grid = get_montar_grafico(y, labels)
        opcao = set_titulo(title)
        
        chart = {
            'type':kind,
            'data':{
                'labels':x,
                'datasets':dados_grid
            },
            'options':opcao
            
        }
        return chart
def get_dados_api_chart(chart):
    url_requisicao = 'https://quickchart.io/chart'
    resposta = requisicao.get(f'{url_requisicao}?c={str(chart)}')
    return resposta.content

def save_image(path,content):
    with open(path, 'wb') as image:
        image.write(content)
    

def display_image(path):
    img_pil = Image.open(path)
    display(img_pil)
    
y_dados1 = []
for informacao_obtida in dados_solicitados[1:10]:
    y_dados1.append(informacao_obtida[CONFIRMADOS])

y_dados2 = []
for informacao_obtida in dados_solicitados[1:10]:
    y_dados2.append(informacao_obtida[RECUPERADOS])
    
    
labels = ['Recuperados','Confirmados']

    
x_dados_barra = []
for informacao_obtida in dados_solicitados[1:10]:
    x_dados_barra.append(informacao_obtida[DATA].strftime('%d/%m/%Y'))

chart = create_chart(x_dados_barra, [y_dados1, y_dados2], labels, title='Grafico ConfirmadosXRecuperados')
chart_content = get_dados_api_chart(chart)
save_image('grafico.png', chart_content)
display_image('grafico.png')

def get_api_gerar_qr(link):
    text = quote(link)
    url_requisicao_qr = 'https://quickchart.io/qr'
    resposta = requisicao.get(f'{url_requisicao_qr}?text={text}') 
    return resposta.content

url_requisicao = 'https://quickchart.io/chart'
link = f'{url_requisicao}?c={str(chart)}'
save_image('qr-code.png', get_api_gerar_qr(link))
display_image('qr-code.png')
