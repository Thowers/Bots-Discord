import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands, tasks
from discord import ui
import datetime

class CryptoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = 'https://coinmarketcap.com'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.precios_anteriores = {}
        self.historico = {}
        self.botones_mensaje_id = {}  # Guarda el ID del mensaje de botones por canal
        self.embeds_mensaje_id = {}   # Guarda el ID del mensaje de embeds por canal
        self.actualizacion.start()

    def crypto_data(self, top=100):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code != 200:
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        tabla = soup.find('table')
        filas = tabla.find_all('tr')[1:top+1] if tabla else []

        data = []
        for fila in filas:
            nombre = fila.find('p', class_='sc-65e7f566-0 iPbTJf coin-item-name')
            logo = fila.find('img', class_='coin-logo')
            precio_td = fila.find('td', style="text-align:end")
            precio = precio_td.find('span') if precio_td else None
            market_cap = fila.find('span', class_='sc-11478e5d-1 jfwGHx')

            if nombre and logo and precio and market_cap:
                try:
                    data.append({
                        'nombre': nombre.text.strip(),
                        'logo': logo.get('src'),
                        'precio': float(precio.text.strip().replace('$', '').replace(',', '')),
                        'market_cap': market_cap.text.strip()
                    })
                except ValueError:
                    continue
        return data

    @tasks.loop(seconds=30)
    async def actualizacion(self):
        await self.bot.wait_until_ready()
        for guild in self.bot.guilds:
            canal = discord.utils.get(guild.text_channels, name="cryptos")
            if canal and canal.permissions_for(guild.me).send_messages:
                if canal.id not in self.botones_mensaje_id and canal.id not in self.embeds_mensaje_id:
                    try:
                        await canal.purge()
                    except discord.Forbidden:
                        print(f"Permiso denegado para borrar mensajes en {canal.name} de {guild.name}.")
                        continue
                data = self.crypto_data(top=10)
                embeds = []
                nombres = []

                for item in data:
                    nombre = item['nombre']
                    logo = item['logo']
                    precio = item['precio']
                    market_cap = item['market_cap']

                    if nombre not in self.historico:
                        self.historico[nombre] = []
                    # Guardar tupla (precio, hora)
                    hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
                    self.historico[nombre].append((precio, hora_actual))
                    if len(self.historico[nombre]) > 10:
                        self.historico[nombre] = self.historico[nombre][-10:]

                    precio_anterior = self.precios_anteriores.get(nombre)
                    self.precios_anteriores[nombre] = precio

                    if precio_anterior is None:
                        cambio = "🔄 Nuevo dato"
                        valor_anterior_str = "N/A"
                    elif precio > precio_anterior:
                        cambio = "📈 Subió"
                        valor_anterior_str = f"${precio_anterior:.2f}"
                    elif precio < precio_anterior:
                        cambio = "📉 Bajó"
                        valor_anterior_str = f"${precio_anterior:.2f}"
                    else:
                        cambio = "⏸ Sin cambio"
                        valor_anterior_str = f"${precio_anterior:.2f}"

                    if precio_anterior is None:
                        color = discord.Color.greyple() 
                    elif precio > precio_anterior:
                        color = discord.Color.green()
                    elif precio < precio_anterior:
                        color = discord.Color.red()
                    else:
                        color = discord.Color.gold() 

                    embed = discord.Embed(
                        title=f"{nombre}",
                        description=(
                            f"💵 **Precio actual:** ${precio:.2f}\n"
                            f"⏮ **Valor anterior:** {valor_anterior_str}\n"
                            f"📊 **Cambio:** {cambio}\n"
                            f"💰 **Market Cap:** {market_cap}"
                        ),
                        color=color
                    )
                    embed.set_thumbnail(url=logo)
                    embeds.append(embed)
                    nombres.append(nombre)

                class View(ui.View):
                    def __init__(self, nombres, cog):
                        super().__init__(timeout=None)
                        self.cog = cog
                        for nombre in nombres:
                            self.add_item(self.Boton(nombre, self.cog))

                    class Boton(ui.Button):
                        def __init__(self, nombre, cog):
                            super().__init__(label=nombre, style=discord.ButtonStyle.primary, custom_id=nombre)
                            self.nombre = nombre
                            self.cog = cog

                        async def callback(self, interaction: discord.Interaction):
                            historico = self.cog.historico.get(self.nombre)
                            if not historico:
                                texto = "No hay datos disponibles."
                            else:
                                texto = f"**Histórico de {self.nombre}**\n"
                                texto += "\n".join([f"{idx+1}. ${p:.2f} a las {h}" for idx, (p, h) in enumerate(historico)])
                            try:
                                await interaction.user.send(texto)                               
                            except discord.Forbidden:
                                await interaction.response.send_message("No pude enviarte mensaje privado. ¿Tienes los DMs abiertos?", ephemeral=True)

                # Enviar los botones solo si no existe el mensaje
                if canal.id not in self.botones_mensaje_id:
                    view = View(nombres, self)
                    mensaje_botones = await canal.send("Selecciona una moneda para ver su histórico:", view=view)
                    self.botones_mensaje_id[canal.id] = mensaje_botones.id

                # Editar o enviar los mensajes de embeds en bloques de 10
                try:
                    if canal.id in self.embeds_mensaje_id:
                        mensaje_embeds = await canal.fetch_message(self.embeds_mensaje_id[canal.id])
                        await mensaje_embeds.edit(embeds=embeds)
                    else:
                        mensaje_embeds = await canal.send(embeds=embeds)
                        self.embeds_mensaje_id[canal.id] = mensaje_embeds.id
                except discord.HTTPException as e:
                    print(f"Error al enviar o editar embeds: {e}")

    @actualizacion.before_loop
    async def before_actualizacion(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(CryptoCog(bot))