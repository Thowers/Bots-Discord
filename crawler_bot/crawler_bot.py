import requests
from bs4 import BeautifulSoup
from discord.ext import commands
class CryptoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = 'https://coinmarketcap.com'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    @commands.command(name='crypto')
    async def crypto(self, ctx, top: int = 20):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code != 200:
            return await ctx.send("Error al acceder a CoinMarketCap.")            
        soup = BeautifulSoup(response.text, 'html.parser')
        tabla = soup.find('table')
        if not tabla:
            return await ctx.send("No se encontró la tabla de criptomonedas.")       
        filas = tabla.find_all('tr')[1:top+1]
        if not filas:
            return await ctx.send("No se encontraron filas en la tabla.")
        mensajes = []
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
                mensajes.append(f"Cripto: {nombre} | Precio: {precio} | Logo: {logo} | Market Cap: {market_cap}")
        await ctx.send("Top criptomonedas:\n" + "\n".join(mensajes))

async def setup(bot):
    await bot.add_cog(CryptoCog(bot))
