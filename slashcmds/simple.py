import discord
from discord import app_commands

import balls
import random

class Simple(app_commands.Group):
    
    @app_commands.command(description="Says hello",name="hello")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hey {interaction.user.mention}! This is your first slash command!", ephemeral=True, delete_after=60)

    @app_commands.command(description="Repeats given text")
    @app_commands.describe(text="What do you want to repeat?")
    @app_commands.rename(text="message")
    async def repeat(self, interaction: discord.Interaction, text: str):
        await interaction.response.send_message(text, ephemeral=True, delete_after=60)

    @app_commands.command(description="Returns a random number between 1 and number given (default 10)")
    async def roll(self, interaction: discord.Interaction, num:int = 10):
        await interaction.response.send_message(random.randint(1, num))

    @app_commands.command(description="Pongs")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("pong", ephemeral=True, delete_after=60)

    @app_commands.command(name="8ball",
                          description="Ask the magic 8 ball a question")
    async def ball(self, interaction: discord.Interaction, question: str):
        await interaction.response.send_message(
            balls.ball_answers[random.randint(1, len(balls.ball_answers))],
            ephemeral=True,
            delete_after=60,
        )




async def setup(bot):
    bot.tree.add_command(Simple(name="simple", description="Simple commands"))