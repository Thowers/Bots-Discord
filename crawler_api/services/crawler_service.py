import requests
from bs4 import BeautifulSoup

class CrawlerService:
    def get_data(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        url = 'https://lacolonial.com.co/collections/guitarras-electricas' 

        response = requests.get(url, headers=headers)

        print(response.status_code)
        if response.status_code != 200:
            raise Exception(f"Error al realizar la solicitud: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')

        productos = []

        for quote_block in soup.find_all('div', class_='grid-item grid-product'):
            nombre = quote_block.find('div', class_='grid-product__title')
            imagen = quote_block.find('img', class_='grid__image-contain image-style--')
            precio = quote_block.find('span', class_='grid-product__price--current')

            if nombre and imagen and precio:
                productos.append({
                    'nombre': nombre.text.strip(),
                    'imagen': imagen.get('src'),
                    'precio': precio.text.strip()
                })

        return productos
