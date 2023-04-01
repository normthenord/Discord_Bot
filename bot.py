import discord
import random
import os
from dotenv import load_dotenv
import xkcd
# from dotenv.compat import to_env

#dotenv.load_dotenv()

# TOKEN = os.getenv('DISCORD_TOKEN')
load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = '''NormTheNord's Bot Server'''

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    for guild in client.guilds:
        print(guild.name)

    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    print("Receiving message")
    if message.author == client.user:
        print('Message from me')
        return
    if message.content == "!commands":
        await message.channel.send("""current commands:
                                    !roll (number)
                                    !ping
                                    !xkcd or !comic""")
        return
    if message.content == "!roll":
        await message.channel.send(f'Rolling between 1 and 10: {random.randint(1,10)}')
        return
    if message.content == "!ping":
        await message.channel.send('pong!')
        return
    if message.content == "!xkcd" or message.content == "!comic":
        await message.channel.send(xkcd.getRandomComic().getImageLink())

    split = message.content.split(" ")

    for word in split:
        if word.lower() == "normthebot":
            await message.channel.send(f"Hi, {message.author.name}! So Nice to meet you on this grand day!")


    if split[0] == "!roll":
        if split[1].isdigit():
            await message.channel.send(f'Rolling between 1 and {int(split[1])}: {random.randint(1,int(split[1]))}')

client.run(TOKEN)
