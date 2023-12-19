import discord
from discord import app_commands
import requests
import aiohttp

class Meme(app_commands.Group):

    @app_commands.command(description="Returns doc pic")
    async def meme(self, interaction: discord.Interaction):
        await interaction.response.defer()
        print("hi")

        async with aiohttp.ClientSession() as session:
            async with session.get("https://meme-api.com/gimme") as resp:
                data = await resp.json()
                await interaction.followup.send(data['url'])





async def setup(bot):
    bot.tree.add_command(Meme(name="meme", description="Random Meme"))