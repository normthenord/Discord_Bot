import discord
from discord import app_commands

import xkcd as xkcd_module


class Comics(app_commands.Group):

    @app_commands.command(description="Posts a random xkcd comic. Can also provide a number for specific comic")
    async def xkcd(self, interaction: discord.Interaction, comic_num: int = None):
        await interaction.response.defer()
        if comic_num is None:
            comic = xkcd_module.getRandomComic()
            embed = discord.embeds.Embed(title=comic.getTitle())
            embed.set_image(url=comic.getImageLink())
            await interaction.followup.send(embed=embed)

        elif comic_num >= xkcd_module.getLatestComicNum():
            embed = discord.embeds.Embed(title=xkcd_module.getLatestComic().getTitle())
            embed.set_image(url=xkcd_module.getLatestComic().getImageLink())
            embed.set_footer(text="There aren't that many comics yet!")
            await interaction.followup.send(embed=embed)

        elif comic_num > 0 and comic_num <= xkcd_module.getLatestComicNum():
            embed = discord.embeds.Embed(title=xkcd_module.getComic(comic_num).getTitle())
            embed.set_image(url=xkcd_module.getComic(comic_num).getImageLink())
            await interaction.followup.send(embed=embed)



async def setup(bot):
    bot.tree.add_command(Comics(name="comics", description="xkcd comics"))