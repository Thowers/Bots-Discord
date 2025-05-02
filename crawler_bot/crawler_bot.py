import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
url = 'https://coinmarketcap.com' 

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

tabla = soup.find('table')

if tabla:
    filas = tabla.find_all('tr')[1:]
    for fila in filas: 
        nombre = fila.find('p', class_='sc-65e7f566-0 iPbTJf coin-item-name')
        logo = fila.find('img', class_='coin-logo')
        precio_td = fila.find('td', style="text-align:end")
        precio = precio_td.find('span') if precio_td else None
        market_cap = fila.find('span', class_='sc-11478e5d-1 jfwGHx')


        if nombre and logo and precio and market_cap:
            nombre = nombre.text.strip()
            logo = logo.get('src')
            precio = precio.text.strip()
            market_cap = market_cap.text.strip()
            print(f"Cripto: {nombre} | Precio: {precio} | Logo: {logo} | Market Cap: {market_cap}")
else:
    print("No se encontró la tabla.")