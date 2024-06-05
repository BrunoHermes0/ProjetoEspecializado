import requests

# Definindo o URL do host
url = 'http://localhost:5001/resumo'

# Definindo os dados a serem enviados no POST
data = {
    'pos_carA': 'B1',
    'ang_carA': '182.18',
    'pos_carV': 'C3',
    'ang_carV': '19.12'
}

# Fazendo a solicitação POST
resposta = requests.post(url, json=data)

# Verificando a resposta
if resposta.status_code == 200:
    print('Dados no webservice')
else:
    print("Falha ao enviar os dados para o web service:", resposta.status_code)