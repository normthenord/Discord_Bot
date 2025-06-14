import discord
from discord import app_commands
import aiohttp
import requests

from utils.database import database

class AI(app_commands.Group):

    def __init__(self, name: str, description: str):
        super().__init__(name=name, description=description)
        self.db = database()

    @app_commands.command(description="Get a single generated response")
    async def one_off(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            url = "http://192.168.0.176:11434/api/generate"
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": "llama3.2",
                "prompt": f"{prompt}. Try to make your response 2000 characters or less",
                "stream": False  # Set to True if you want streaming output
            }

            try:
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                response_string = data['response']
                if len(response_string) > 2000:
                    response_string = response_string[:2000]
                await interaction.followup.send(response_string)
            except requests.RequestException as e:
                await interaction.followup.send(f"Error: Server probably asleep")

    @app_commands.command(description="Chat with a bot using past chat history")
    async def chat(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        await interaction.followup.send(self.db.chat(str(interaction.user.id), prompt=prompt))

    @app_commands.command(description="Delete chat history")
    async def delete_chat(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.db.delete_convo(str(interaction.user.id))
        await interaction.followup.send("Deleted convo")



    @app_commands.command(description="Delete history from last 'within_minutes'")
    async def delete_recent(self, interaction: discord.Interaction, within_minutes: int):
        await interaction.response.defer()
        try: 
            self.db.delete_recent_convo(user_id=str(interaction.user.id), within_minutes=within_minutes)
        except Exception as e:
            print(e)
        await interaction.followup.send(f"Deleted {within_minutes} minutes from {interaction.user.name} conversation")


async def setup(bot):
    bot.tree.add_command(AI(name="ai", description="AI commands"))
