from discord.ext import commands
import discord

import aiohttp

class Animals(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def dog(self, ctx: commands.Context):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://dog.ceo/api/breeds/image/random") as resp:
                data = await resp.json()
                embed = discord.Embed(title = "Woof")
                embed.set_image(url=data['message'])
                embed.set_footer(text="dog.ceo API")

                await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Animals(bot))