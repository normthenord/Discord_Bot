from discord.ext import commands


def is_bot(msg):
    return msg.author.bot

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
    async def purge_bot(self,ctx:commands.Context):
        await ctx.channel.purge(limit=100,check=is_bot)

    @commands.command()
    @commands.check(commands.is_owner())
    async def purge_all(self,ctx:commands.Context):
        await ctx.channel.purge(limit=100)

    @commands.command()
    @commands.check(commands.is_owner())
    async def purge_commands(self,ctx:commands.Context):
        await ctx.channel.purge(limit=100, check=is_command)

    # @commands.command()
    # @commands.check(commands.is_owner())
    # async def delete_commands(self,ctx:commands.Context):
    #     prev_message = list()
    #     async for msg in ctx.channel.history(limit=15):
    #         if msg.author.bot:
    #             prev_message.append(msg)
    #     await ctx.channel.delete_messages(prev_message)


async def setup(bot):
    await bot.add_cog(Admin(bot))