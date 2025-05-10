import discord
from discord.ext import commands
from .logica_insta_bot import obtener_ultimos_posts

class InstagramBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="igposts", help="Muestra los últimos posts de un perfil de Instagram. Uso: !igposts usuario cantidad")
    async def igposts(self, ctx, usuario: str, cantidad: int = 3):
        await ctx.typing()
        try:
            posts, solicitudes = obtener_ultimos_posts(usuario, cantidad)
            await ctx.send(f"Solicitudes realizadas a Instagram: {solicitudes}")
            if not posts:
                await ctx.send("No se encontraron posts o el perfil es privado.")
                return
            for post in posts:
                embed = discord.Embed(
                    title=f"Post de @{usuario}",
                    description=post["caption"] or "Sin descripción",
                    color=discord.Color.purple()
                )
                embed.add_field(name="Fecha", value=post["fecha"])
                embed.add_field(name="URL", value=post["url"], inline=False)
                embed.set_image(url=post["url"])
                await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error al obtener los posts: {e}")

async def setup(bot):
    await bot.add_cog(InstagramBot(bot))