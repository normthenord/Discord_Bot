import random

import xkcd

import discord
from discord.ext import commands
import os


from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = '''NormTheNord's Bot Server'''

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def test(ctx, *args):
    arguments = ' '.join(args)
    await ctx.send(arguments)

@bot.command()
async def roll(ctx, arg=10):
    await ctx.send(f'Rolling between 1 and {arg}: {random.randint(1,int(arg))}')

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command(name="xkcd")
async def comic(ctx):
    await ctx.send(xkcd.getRandomComic().getImageLink())

@bot.command()
async def comic(ctx):
    await ctx.send(xkcd.getRandomComic().getImageLink())



@bot.command()
async def commands(ctx):
    await ctx.send("""current commands:
                                    !test {statement to be repeated}
                                    !roll {number}
                                    !ping
                                    !xkcd or !comic
                                    !hello""")

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.message.author.name}')




@bot.event
async def on_ready():
    for guild in client.guilds:
        print(guild.name)

    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    print("Receiving message")
    if message.author == client.user:
        print('Message from me')
        return
    

    if message.content.lower() == "bye":
        await message.channel.send(commands.bye(message))
        return
    
    split = message.content.split(" ")

    for word in split:
        if word.lower() == "normthebot":
            await message.channel.send(f"Hi, {message.author.name}! So Nice to meet you on this grand day!")

    await bot.process_commands(message)




bot.run(TOKEN)