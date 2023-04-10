from discord.ext import commands

import random
import balls


class Simple(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Repeats given text")
    async def repeat(self, ctx, *args):
        arguments = ' '.join(args)
        await ctx.reply(arguments)

    @commands.command(help="Returns a random number between 1 and number given (default 10)")
    async def roll(self, ctx, arg=10):
        # await ctx.reply(f'Rolling between 1 and {arg}: {random.randint(1,int(arg))}')
        await ctx.reply(random.randint(1,int(arg)))

    @commands.command(help="Pongs")
    async def ping(self, ctx):
        await ctx.reply("pong")

    # @commands.command(help="Responds hello")
    # async def hello(self, ctx):
    #     await ctx.send(f'Hello, {ctx.message.author.name}')


    @commands.command(name="8ball",
             help="Ask the magic 8 ball a question")
    async def ball(self, ctx):
        await ctx.reply(balls.ball_answers[random.randint(1,int(len(balls.ball_answers)))])


async def setup(bot):
    await bot.add_cog(Simple(bot))