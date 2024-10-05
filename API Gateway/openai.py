import requests

# Defina sua chave de API
API_KEY = 'gfdfdgA'

# URL da API do ChatGPT
url = 'https://api.openai.com/v1/chat/completions'

# Cabeçalhos da requisição
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json',
}

# Corpo da requisição
data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "Dados retornados da API"}
    ],
    "max_tokens": 50    
}

# request
response = requests.post(url, headers=headers, json=data)

# response
if response.status_code == 200:
    response_data = response.json()
    message = response_data['choices'][0]['message']['content']
    print(message)
else:
    print("Erro:", response.status_code, response.text)
