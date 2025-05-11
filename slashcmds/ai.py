import discord
from discord import app_commands
import aiohttp
import settings
import requests



class AI(app_commands.Group):

    @app_commands.command(description="Get a single generated response")
    async def generate(self, interaction: discord.Interaction, prompt: str):
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

   

    
async def setup(bot):
    bot.tree.add_command(AI(name="ai", description="AI commands"))
