import requests
from bs4 import BeautifulSoup

class CrawlerService:
    def get_data(self):
        url = "https://coinmarketcap.com/"
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/58.0.3029.110 Safari/537.3'
            )
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception("Error al acceder a CoinMarketCap.")

        soup = BeautifulSoup(response.text, 'html.parser')
        tabla = soup.find('table')
        if not tabla:
            raise Exception("No se encontró la tabla de criptomonedas.")

        filas = tabla.find_all('tr')[1:]
        if not filas:
            raise Exception("No se encontraron filas en la tabla.")

        datos = []
        for fila in filas:
            nombre_tag = fila.find('p', class_='sc-65e7f566-0 iPbTJf coin-item-name')
            logo_tag = fila.find('img', class_='coin-logo')
            precio_td = fila.find('td', style="text-align:end")
            precio_tag = precio_td.find('span') if precio_td else None
            market_cap_tag = fila.find('span', class_='sc-11478e5d-1 jfwGHx')

            if nombre_tag and logo_tag and precio_tag and market_cap_tag:
                datos.append({
                    'nombre': nombre_tag.text.strip(),
                    'logo': logo_tag.get('src'),
                    'precio': precio_tag.text.strip(),
                    'market_cap': market_cap_tag.text.strip()
                })

        return datos