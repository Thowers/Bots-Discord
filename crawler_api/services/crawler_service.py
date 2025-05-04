import requests
from bs4 import BeautifulSoup

class CrawlerService:
    def get_data(self):
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/58.0.3029.110 Safari/537.3'
            )
        }
        url = 'https://lacolonial.com.co/collections/guitarras-electricas'
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            raise Exception(f"HTTP {resp.status_code}")

        soup = BeautifulSoup(resp.text, 'html.parser')
        productos = []
        for bloc in soup.find_all('div', class_='grid-item grid-product'):
            n = bloc.find('div', class_='grid-product__title')
            img = bloc.find('img', class_='grid__image-contain image-style--')
            p = bloc.find('span', class_='grid-product__price--current')
            if n and img and p:
                productos.append({
                    'nombre': n.text.strip(),
                    'imagen': 'https:' + img.get('src'),
                    'precio': p.text.strip()
                })
        return productos
