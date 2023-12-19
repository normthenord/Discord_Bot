import discord
from discord import app_commands
import requests
import aiohttp

class Meme(app_commands.Group):

    @app_commands.command(description="Returns random memes from Reddit")
    async def meme(self, interaction: discord.Interaction, count:int = 1):
        
        if count > 5:
            count = 5
        elif count < 1:
            count = 1
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            # api_url=f"https://meme-api.com/gimme/{count}"
            # async with aiohttp.ClientSession() as session:
            api_url=f"https://meme-api.com/gimme/{count}"
            async with session.get(api_url) as resp:
                data = await resp.json()
                urls = []
                for meme in data['memes']:
                    urls.append(meme['url'])
                await interaction.followup.send(" ".join(urls))




async def setup(bot):
    bot.tree.add_command(Meme(name="meme", description="Random Memes"))