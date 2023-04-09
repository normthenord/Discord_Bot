from discord.ext import commands
import discord

import aiohttp
import requests

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

    @commands.command()
    async def cat(self, ctx: commands.Context, *, args=""):
        url = "https://cataas.com/cat?json=true"
        if args != "":
            prompt = "".join(args)
            prompt = prompt.replace(" ", "%20")
            url = f'https://cataas.com/cat/says/{prompt}?json=true'
        resp = requests.get(url)
        data = resp.json()
        embed = discord.Embed(title = "Meow")
        embed.set_image(url=f"https://cataas.com{data['url']}")
        embed.set_footer(text="Cataas")
        await ctx.reply(embed=embed)
                    
                    

async def setup(bot):
    await bot.add_cog(Animals(bot))