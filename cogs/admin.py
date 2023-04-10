from discord.ext import commands

import datetime



def is_command(msg):
    return msg.content.startswith("!")


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
    async def purge_bot(self,ctx:commands.Context, arg:int = 100):
        await ctx.channel.purge(limit=arg,check=lambda msg: msg.author.bot)

    @commands.command()
    @commands.check(commands.is_owner())
    async def purge_all(self,ctx:commands.Context, arg:int = 100):
        await ctx.channel.purge(limit=arg)

    @commands.command()
    @commands.check(commands.is_owner())
    async def purge_commands(self,ctx:commands.Context, arg:int = 100):
        await ctx.channel.purge(limit=arg, check=lambda msg: msg.content.startswith("!"))
    
    @commands.command()
    @commands.check(commands.is_owner())
    async def purge_hour(self,ctx:commands.Context):
        await ctx.channel.purge(
            after=datetime.datetime.now() - datetime.timedelta(hours=1)
        )


async def setup(bot):
    await bot.add_cog(Admin(bot))