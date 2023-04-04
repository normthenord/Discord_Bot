from discord.ext import commands

import xkcd as xkcd_module


class Comics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Posts a random xkcd comic. Can also provide a number for specific comic")
    async def xkcd(self, ctx, arg = None):
        if arg == None:
            comic = xkcd_module.getRandomComic()
            await ctx.send(f'{comic.getTitle()}\n')
            await ctx.send(comic.getImageLink())
        elif int(arg) >= xkcd_module.getLatestComicNum():
            await ctx.send(f'{xkcd_module.getLatestComic().getTitle()}\n')
            await ctx.send(xkcd_module.getLatestComic().getImageLink())
        elif int(arg) > 0 and int(arg) <= xkcd_module.getLatestComicNum():
            await ctx.send(f'{xkcd_module.getComic(int(arg)).getTitle()}\n')
            await ctx.send(xkcd_module.getComic(int(arg)).getImageLink())

    @commands.command(help="Posts a random xkcd comic. Can also provide a number for specific comic")
    async def comic(self, ctx, arg = None):
        if arg == None:
            comic = xkcd_module.getRandomComic()
            await ctx.send(f'{comic.getTitle()}\n')
            await ctx.send(comic.getImageLink())
        elif int(arg) >= xkcd_module.getLatestComicNum():
            await ctx.send(f'{xkcd_module.getLatestComic().getTitle()}\n')
            await ctx.send(xkcd_module.getLatestComic().getImageLink())
        elif int(arg) > 0 and int(arg) <= xkcd_module.getLatestComicNum():
            await ctx.send(f'{xkcd_module.getComic(int(arg)).getTitle()}\n')
            await ctx.send(xkcd_module.getComic(int(arg)).getImageLink())


async def setup(bot):
    await bot.add_cog(Comics(bot))