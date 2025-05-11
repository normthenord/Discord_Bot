#!/usr/bin/env python3
import asyncio

import os
import datetime

import xkcd

import discord
from discord.ext import commands, tasks


from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = '''NormTheNord's Bot Server'''

BOT_TEST_CHANNEL = 775081202805768223
GENERAL_CHANNEL = 775071141253349409

EVERY_HOUR = [datetime.time(hour=i, tzinfo=datetime.timezone.utc) for i in range(24)]



intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f'cogs.{filename[:-3]}')

    for filename in os.listdir("./slashcmds"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f'slashcmds.{filename[:-3]}')


#############Looping Tasks#################

@tasks.loop(time = EVERY_HOUR)
async def comic_hour():
    channel = bot.get_channel(BOT_TEST_CHANNEL)
    comic = xkcd.getRandomComic()
    await channel.send(f'{comic.getTitle()}\n')
    await channel.send(comic.getImageLink())
    await channel.send("Random hourly comic post!")

# @tasks.loop(time =datetime.time(hour= 16, minute=0,tzinfo=datetime.timezone.utc))
@tasks.loop(time =datetime.time(hour= 16, minute=0,tzinfo=datetime.timezone.utc))
async def comic_daily():
    channel = bot.get_channel(GENERAL_CHANNEL)
    comic = xkcd.getLatestComic()

    link = comic.getImageLink()
    prev_message = []
    async for msg in channel.history(limit=100):
        if msg.content == link:
            print("Already sent daily comic")
            return
    await channel.send(f'{comic.getTitle()}\n')
    await channel.send(link)
    await channel.send("Enjoy your daily comic!")


@bot.event
async def on_command_error(ctx,error):
    print(error)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(guild.name)
    comic_hour.start()
    comic_daily.start()

    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        print('Message from me')
        return
    print("Receiving message")
      
    await bot.process_commands(message)



async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())
