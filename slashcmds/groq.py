import discord
from discord import app_commands

import slashcmds.groq as groq
import aiohttp

import groq

import settings

import requests
LIMEWIRE_KEY = settings.LIMEWIRE_KEY

class AI(app_commands.Group):

    @app_commands.command(description="Get AI Generated image")
    async def image(self, interaction: discord.Interaction, img_prompt: str):
        await interaction.response.defer()

        async with aiohttp.ClientSession() as session:
            url = "https://api.limewire.com/api/image/generation"
            header = {"Content-Type": "application/json",
                      "X-Api-Version": "v1",
                      "Accept": "application/json",
                      "Authorization": f"Bearer {LIMEWIRE_KEY}"}

            payload = payload = {"prompt": img_prompt,
                                 "aspect_ratio": "1:1"}

            r = requests.post(url=url, json=payload, headers=header)
            data = r.json()
            print(f"Credits remaining: {data['credits_remaining']}")
            await interaction.followup.send(data['data'][0]['asset_url'])


    @app_commands.command(description="mixtral-8x7b-32768")
    async def chat(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            try:
                client = groq.Client(api_key=settings.GROQ_KEY)
                self.result = client.chat.completions.create(
                    messages=[{
                        "role": "user",
                        "content": prompt,
                    }
                    ],
                    model="mixtral-8x7b-32768",
                )
                print(f"Total tokens used: {self.result.usage.total_tokens}")
                await interaction.followup.send(self.result.choices[0].message.content)
            except Exception as e:
                print(e)


async def setup(bot):
    bot.tree.add_command(AI(name="ai", description="Groq commands"))
