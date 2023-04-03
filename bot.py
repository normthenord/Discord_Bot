import balls


import random
import os
import datetime

import xkcd

import aiohttp

import discord
from discord.ext import commands, tasks


from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = '''NormTheNord's Bot Server'''

GPT_KEY = os.getenv('GPT_API_KEY')

BOT_TEST_CHANNEL = 775081202805768223
GENERAL_CHANNEL = 775071141253349409

EVERY_HOUR = [datetime.time(hour=i, tzinfo=datetime.timezone.utc) for i in range(24)]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


####### gpt-3.5-turbo
@bot.command(help="GPT 3.5 Turbo -- only works in gpt_bot")
async def gpt(ctx: commands.Context, *, prompt: str):
    # if ctx.channel.id != 1092256153968332800:
    #     return
    async with aiohttp.ClientSession() as session:

        conversation = [{"role": "system", "content": "I am a friendly chatbot"}]

        prev_message = []
        async for msg in ctx.channel.history(limit=15):
            if msg.content.startswith("!gpt ") == True and msg.author.id == ctx.author.id:
                prev_message.append({'role': 'user', 'content': msg.content[5:]})
        prev_message.reverse()
        for message in prev_message:
            conversation.append(message)
    
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": conversation,
            "temperature": 0.5,
            "max_tokens": 500,
            "presence_penalty": 0,
            "frequency_penalty": 0,

        }
        headers = {"Authorization": f'Bearer {GPT_KEY}'}
        async  with ctx.typing():
            async with session.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers) as resp:
                response = await resp.json()
                # embed = discord.Embed(title="Chat GPT's Response:",
                #                     description=response['choices'][0]['message']['content'])
                await ctx.reply(response['choices'][0]['message']['content'])
                print("GPT total tokens: " + str(response['usage']['total_tokens']))


# ### Davinci 3
# @bot.command(help="Davinci 3")
# async def gpt(ctx: commands.Context, *, prompt: str):
    # async with aiohttp.ClientSession() as session:
    #     payload = {
    #         "model": "text-davinci-003",
    #         "prompt": prompt,
    #         "temperature": 0.5,
    #         "max_tokens": 500,
    #         "presence_penalty": 0,
    #         "frequency_penalty": 0,
    #         "best_of": 1,

    #     }
    #     headers = {"Authorization": f'Bearer {GPT_KEY}'}
    #     async with session.post("https://api.openai.com/v1/completions", json=payload, headers=headers) as resp:
    #         response = await resp.json()
    #         embed = discord.Embed(title="Chat GPT's Response:",
    #                               description=response["choices"][0]["text"])
    #         await ctx.reply(embed = embed)



@bot.command(help="Repeats given text")
async def test(ctx, *args):
    arguments = ' '.join(args)
    await ctx.send(arguments)

@bot.command(help="Returns a random number between 1 and number given (default 10)")
async def roll(ctx, arg=10):
    await ctx.send(f'Rolling between 1 and {arg}: {random.randint(1,int(arg))}')

@bot.command(help="Pongs")
async def ping(ctx):
    await ctx.send("pong")

@bot.command(name="xkcd",
             help="Posts a random xkcd comic. Can also provide a number for specific comic")
async def comic(ctx, arg = None):
    if arg == None:
        comic = xkcd.getRandomComic()
        await ctx.send(f'{comic.getTitle()}\n')
        await ctx.send(comic.getImageLink())
    elif int(arg) >= xkcd.getLatestComicNum():
        await ctx.send(f'{xkcd.getLatestComic().getTitle()}\n')
        await ctx.send(xkcd.getLatestComic().getImageLink())
    elif int(arg) > 0 and int(arg) <= xkcd.getLatestComicNum():
        await ctx.send(f'{xkcd.getComic(int(arg)).getTitle()}\n')
        await ctx.send(xkcd.getComic(int(arg)).getImageLink())

@bot.command(help="Posts a random xkcd comic. Can also provide a number for specific comic")
async def comic(ctx, arg = None):
    if arg == None:
        comic = xkcd.getRandomComic()
        await ctx.send(f'{comic.getTitle()}\n')
        await ctx.send(comic.getImageLink())
    elif int(arg) >= xkcd.getLatestComicNum():
        await ctx.send(f'{xkcd.getLatestComic().getTitle()}\n')
        await ctx.send(xkcd.getLatestComic().getImageLink())
    elif int(arg) > 0 and int(arg) <= xkcd.getLatestComicNum():
        await ctx.send(f'{xkcd.getComic(int(arg)).getTitle()}\n')
        await ctx.send(xkcd.getComic(int(arg)).getImageLink())
    

@bot.command(help="Responds hello")
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.message.author.name}')


@bot.command(name="8ball",
             help="Ask the magic 8 ball a question")
async def ball(ctx):
    await ctx.send(balls.ball_answers[random.randint(1,int(len(balls.ball_answers)))])


@tasks.loop(time = EVERY_HOUR)
async def comic_hour():
    channel = bot.get_channel(BOT_TEST_CHANNEL)
    comic = xkcd.getRandomComic()
    await channel.send(f'{comic.getTitle()}\n')
    await channel.send(comic.getImageLink())
    await channel.send("Random hourly comic post!")

@tasks.loop(time =datetime.time(hour= 18, tzinfo=datetime.timezone.utc))
async def comic_daily():
    channel = bot.get_channel(GENERAL_CHANNEL)
    comic = xkcd.getLatestComic()
    await channel.send(f'{comic.getTitle()}\n')
    await channel.send(comic.getImageLink())
    await channel.send("Enjoy your daily comic!")


@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(guild.name)
    comic_hour.start()
    comic_daily.start()

    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        print('Message from me')
        return
    
    print("Receiving message")
      

    if message.content.lower() == "bye":
        await message.channel.send(commands.bye(message))
        return
    
    split = message.content.split(" ")

    for word in split:
        if word.lower() == "normthebot":
            await message.channel.send(f"Hi, {message.author.name}! So Nice to meet you on this grand day!")

    await bot.process_commands(message)




bot.run(TOKEN)