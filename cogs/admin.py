from discord.ext import commands
import discord

import xkcd as xkcd_module


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(commands.is_owner())
    async def delete(self,ctx:commands.Context, arg: int=1):
        async for msg in ctx.channel.history(limit=arg+1):
            print(f'Deleting {msg.content}')
            await msg.delete()

    @commands.command()
    @commands.check(commands.is_owner())
    async def purge(self,ctx:commands.Context):
        await ctx.channel.purge()


async def setup(bot):
    await bot.add_cog(Admin(bot))