import discord
from discord import app_commands

import openai
import aiohttp

import settings
openai.api_key = settings.GPT_KEY




class AI(app_commands.Group):
    


    @app_commands.command(description="Get AI Generated image (1024*1024) -- max 4 images")
    async def image(self, interaction: discord.Interaction, img_prompt: str, img_num: int = 1):
        await interaction.response.defer()

        async with aiohttp.ClientSession() as session:
            
            response = openai.Image.create(
            prompt=img_prompt,
            n=img_num,
            size="1024x1024"
            )

            embeds = []
            for num in range(img_num):
                embeds.append(discord.Embed(url = "https://normthenord.github.io").set_image(url = response['data'][num]['url']))
            
            await interaction.followup.send(embeds=embeds)



    @app_commands.command(description="Davinci 3")
    async def davinci(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            self.payload = {
                "model": "text-davinci-003",
                "prompt": prompt,
                "temperature": 0.5,
                "max_tokens": 500,
                "presence_penalty": 0,
                "frequency_penalty": 0,
                "best_of": 1,

            }
            self.headers = {"Authorization": f'Bearer {settings.GPT_KEY}'}
            async with session.post("https://api.openai.com/v1/completions", json=self.payload, headers=self.headers) as resp:

                self.response = await resp.json()
                # embed = discord.Embed(title="Chat GPT's Response:",
                #                     description=response["choices"][0]["text"])
                
                await interaction.followup.send(self.response["choices"][0]["text"])




async def setup(bot):
    bot.tree.add_command(AI(name="ai", description="OpenAI commands"))