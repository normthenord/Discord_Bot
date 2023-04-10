import discord
from discord import app_commands

from discord.ext import commands
import openai
import aiohttp
import os

from dotenv import load_dotenv
load_dotenv()

GPT_KEY = os.getenv('GPT_API_KEY')
openai.api_key = GPT_KEY




class AI(app_commands.Group):
    


    # @app_commands.command(description="GPT 3.5 Turbo")
    # async def chat(self, interaction: discord.Interaction, prompt: str):
        
    #     if interaction.channel.id != 1092256153968332800:
    #         await interaction.reply("Must be in ai-chat channel to chat with bot")
    #         return
    #     async with aiohttp.ClientSession() as session:

    #         conversation = [{"role": "system", "content": "I am a friendly chatbot"}]           
            
    #         prev_message = list()
    #         async for msg in interaction.channel.history(limit=15):
    #             if msg.content.startswith("!chat ") == True and msg.author.id == interaction.author.id:
    #                prev_message.append({'role': 'user', 'content': msg.content[5:]})

    #         prev_message.reverse()
    #         for message in prev_message:
    #             conversation.append(message)
        
    #         self.payload = {
    #             "model": "gpt-3.5-turbo",
    #             "messages": conversation,
    #             "temperature": 0.5,
    #             "max_tokens": 500,
    #             "presence_penalty": 0,
    #             "frequency_penalty": 0,
    #         }

    #         self.headers = {"Authorization": f'Bearer {GPT_KEY}'}


    #         async with session.post("https://api.openai.com/v1/chat/completions", json=self.payload, headers=self.headers) as resp:
    #             self.response = await resp.json()
    #             # embed = discord.Embed(title="Chat GPT's Response:",
    #             #                     description=response['choices'][0]['message']['content'])
    #             await interaction.response.send_message(self.response['choices'][0]['message']['content'])
    #             print("GPT total tokens: " + str(self.response['usage']['total_tokens']))


    @app_commands.command(description="Get AI Generated image (1024*1024)")
    async def image(self, interaction: discord.Interaction, img_prompt: str):
        await interaction.response.defer()

        async with aiohttp.ClientSession() as session:
            
            response = openai.Image.create(
            prompt=img_prompt,
            n=1,
            size="1024x1024"
            )
            image_url = response['data'][0]['url']

            
            await interaction.followup.send(image_url)




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
            self.headers = {"Authorization": f'Bearer {GPT_KEY}'}
            async with session.post("https://api.openai.com/v1/completions", json=self.payload, headers=self.headers) as resp:

                self.response = await resp.json()
                # embed = discord.Embed(title="Chat GPT's Response:",
                #                     description=response["choices"][0]["text"])
                
                await interaction.followup.send(self.response["choices"][0]["text"])




async def setup(bot):
    bot.tree.add_command(AI(name="ai", description="OpenAI commands"))