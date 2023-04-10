import discord
from discord import app_commands

import balls
import random

class Simple(discord.app_commands.Group):
    
    @app_commands.command(description="Says hello",name="hello")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hey {interaction.user.mention}! This is your first slash command!", ephemeral=True)

    # @app_commands.command(description="Repeats given text")
    # async def repeat(self, interaction: discord.Interaction, *args):
    #     arguments = ' '.join(args)
    #     await interaction.response.send_message(arguments)

    # @app_commands.command(description="Returns a random number between 1 and number given (default 10)")
    # async def roll(self, interaction: discord.Interaction, arg=10):
    #     await interaction.response.send_message(random.randint(1,int(arg)))

    # @app_commands.command(description="Pongs")
    # async def ping(self, interaction: discord.Interaction):
    #     await interaction.response.send_message("pong")

    # @app_commands.command(description="Responds hello")
    # async def hello(self, interaction: discord.Interaction):
    #     await interaction.response.send_message(f'Hello, {ctx.message.author.name}')


    # @app_commands.command(name="8ball",
    #          description="Ask the magic 8 ball a question")
    # async def ball(self, interaction: discord.Interaction):
    #     await interaction.response.send_message(balls.ball_answers[random.randint(1,int(len(balls.ball_answers)))])




async def setup(bot):
    bot.tree.add_command(Simple(name="hello", description="Says Hello"))