import asyncio
import discord
from discord.ext import commands
from google_bot.modulos.google     import busqueda
from google_bot.modulos.duckduckgo import duckduckgo_search
from google_bot.utils.dedupe       import dedupe_urls

class SearchBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='search', help='Busca en Google y DuckDuckGo, !serch termino de busqueda')
    async def search(self, ctx, *, query: str = None):
        if ctx.channel.name.lower() != "search":
            return await ctx.send("Este comando solo está disponible en el canal #search.")

        if not query:
            return await ctx.send(
                "Uso incorrecto. Debes especificar qué buscar:\n"
                "`!search término de búsqueda`"
            )

        await ctx.typing()

        resultados_google   = asyncio.to_thread(busqueda, query, 15)
        resultados_duck = asyncio.to_thread(duckduckgo_search, query, 15)

        tag_google = [(url, "Google") for url in await resultados_google]
        tag_duck   = [(url, "DuckDuckGo") for url in await resultados_duck]

        resultados= tag_google + tag_duck
        seen = set()
        urls = []
        for url, source in resultados:
            if url not in seen:
                seen.add(url)
                urls.append((url, source))

        if not urls:
            return await ctx.send("No se encontraron resultados.")

        embed = discord.Embed(title=f"Resultados para \"{query}\"",color=discord.Color.blue())

        for i, (url,source) in enumerate(urls[:10], 1):
            embed.add_field(name=f"Resultado {i} [{source}]", value=url, inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SearchBot(bot))