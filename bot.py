import discord
import random
import os\

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = '''NormTheNord's Bot Server'''

client = discord.Client()


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
    if message.content == "!roll":
        await message.channel.send(f'Rolling between 1 and 10: {random.randint(1,10)}')
        return

    split = message.content.split(" ")
    if "NormTheBot" in message.content:
        await message.channel.send(f"Hi, {message.author.name}! So Nice to meet you on this grand day!")

    if split[0] == "!roll":
        if split[1].isdigit():
            await message.channel.send(f'Rolling between 1 and {int(split[1])}: {random.randint(1,int(split[1]))}')

client.run(TOKEN)
