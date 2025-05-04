import os
import threading
from dotenv import load_dotenv

import discord
from discord.ext import commands

from crawler_api.crawler import run_app

load_dotenv()

#--Bot Discord--#
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.dm_messages = True
bot = commands.Bot(command_prefix="!", intents=intents)
bot.load_extension("crawler_bot.crawler_bot")

class CustomBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.load_extension("crawler_bot.crawler_bot")
        #print("✅ Cogs cargados.")

bot = CustomBot()

@bot.event
async def on_ready():
    #print(f"Bot conectado como {bot.user}")
    #print("Comandos registrados:", [c.name for c in bot.commands])
    for guild in bot.guilds:
        canal = discord.utils.get(guild.text_channels, name="general")
        if canal and canal.permissions_for(guild.me).send_messages:
            try:
                await canal.purge(limit=None)
                await canal.send("Bot en linea")
            except discord.Forbidden:
                print(f"Permissão negada para enviar mensagens em {canal.name} no servidor {guild.name}. No se porque esta en portugues")

def run_bot():
    bot.run(TOKEN)

if __name__ == "__main__":
    threading.Thread(target=run_app, daemon=True).start()
    run_bot()