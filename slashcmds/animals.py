
import discord
from discord import app_commands

import aiohttp
import requests


class Animals(app_commands.Group):
    
    @app_commands.command(description="Returns doc pic")
    async def dog(self, interaction: discord.Interaction):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://dog.ceo/api/breeds/image/random") as resp:
                data = await resp.json()
                embed = discord.Embed(title = "Woof")
                embed.set_image(url=data['message'])
                embed.set_footer(text="dog.ceo API")

                await interaction.followup.send(embed=embed)

    @app_commands.command(description="Returns cat pic. Can provide a phrase for cat to say (no punctuation)")
    async def cat(self, interaction: discord.Interaction, phrase:str =""):
        await interaction.response.defer()
        url = "https://cataas.com/cat?json=true"
        if phrase != "":
            phrase = phrase.replace(" ", "%20")
            url = f'https://cataas.com/cat/says/{phrase}?json=true'
        resp = requests.get(url)
        data = resp.json()
        embed = discord.Embed(title = "Meow")
        embed.set_image(url=f"https://cataas.com{data['url']}")
        embed.set_footer(text="Cataas")
        await interaction.followup.send(embed=embed)




async def setup(bot):
    bot.tree.add_command(Animals(name="animal", description="Random Animal Pics"))