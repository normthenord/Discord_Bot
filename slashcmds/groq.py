import discord
from discord import app_commands

import slashcmds.groq as groq
import aiohttp

import groq

import settings


class AI(app_commands.Group):

    # @app_commands.command(description="Get AI Generated image (1024*1024) -- max 4 images")
    # async def image(self, interaction: discord.Interaction, img_prompt: str, img_num: int = 1):
    #     await interaction.response.defer()

    #     async with aiohttp.ClientSession() as session:

    #         response = openai.Image.create(
    #         prompt=img_prompt,
    #         n=img_num,
    #         size="1024x1024"
    #         )

    #         embeds = []
    #         for num in range(img_num):
    #             embeds.append(discord.Embed(url = "https://normthenord.github.io").set_image(url = response['data'][num]['url']))

    #         await interaction.followup.send(embeds=embeds)

    @app_commands.command(description="mixtral-8x7b-32768")
    async def chat(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
 
            client = groq.Client(api_key=settings.GROQ_Key)
            self.result = client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": prompt,
                }
                ],
                model="mixtral-8x7b-32768",
            )

            await interaction.followup.send(self.result.choices[0].message.content)

async def setup(bot):
    bot.tree.add_command(AI(name="ai", description="Groq commands"))
