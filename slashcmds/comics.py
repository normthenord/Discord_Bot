import discord
from discord import app_commands

import xkcd as xkcd_module


class Comics(app_commands.Group):

    @app_commands.command(description="Posts a random xkcd comic. Can also provide a number for specific comic")
    async def xkcd(self, interaction: discord.Interaction, comic_num: int = None):
        await interaction.response.defer()
        if comic_num == None:
            comic = xkcd_module.getRandomComic()
            embed = discord.embeds.Embed(title=comic.getTitle())
            embed.set_image(url=comic.getImageLink())
            await interaction.followup.send(embed=embed)
            # await interaction.followup.send(f'{comic.getTitle()}\n')
            # await interaction.followup.send(comic.getImageLink())
        elif int(comic_num) >= xkcd_module.getLatestComicNum():
            embed = discord.embeds.Embed(title=xkcd_module.getLatestComic().getTitle())
            embed.set_image(url=xkcd_module.getLatestComic().getImageLink())
            embed.set_footer(text="There aren't that many comics yet!")
            await interaction.followup.send(embed=embed)
            # await interaction.followup.send(f'{xkcd_module.getLatestComic().getTitle()}\n')
            # await interaction.followup.send(xkcd_module.getLatestComic().getImageLink())
        elif int(comic_num) > 0 and int(comic_num) <= xkcd_module.getLatestComicNum():
            embed = discord.embeds.Embed(title=xkcd_module.getComic(int(comic_num)).getTitle())
            embed.set_image(url=xkcd_module.getComic(int(comic_num)).getImageLink())
            await interaction.followup.send(embed=embed)
            # await interaction.followup.send(f'{xkcd_module.getComic(int(comic_num)).getTitle()}\n')
            # await interaction.followup.send(xkcd_module.getComic(int(comic_num)).getImageLink())


async def setup(bot):
    bot.tree.add_command(Comics(name="comics", description="xkcd comics"))