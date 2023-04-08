from discord.ext import commands
import discord

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dm(self, ctx:commands.Context, *, args):
        await ctx.message.author.send(args)


async def setup(bot):
    await bot.add_cog(Test(bot))