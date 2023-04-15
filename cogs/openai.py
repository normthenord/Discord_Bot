from discord.ext import commands
import openai
import aiohttp
import os

import settings
openai.api_key = settings.GPT_KEY


class OpenAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(help="GPT 3.5 Turbo")
    async def chat(self, ctx: commands.Context, *, prompt: str):
        
        if ctx.channel.id != 1092256153968332800:
            await ctx.reply("Must be in ai-chat channel to chat with bot")
            return
        async with aiohttp.ClientSession() as session:

            conversation = [{"role": "system", "content": "I am a friendly chatbot"}]           
            
            prev_message = list()
            async for msg in ctx.channel.history(limit=15):
                if msg.content.startswith("!chat ") == True and msg.author.id == ctx.author.id:
                   prev_message.append({'role': 'user', 'content': msg.content[5:]})

            prev_message.reverse()
            for message in prev_message:
                conversation.append(message)
        
            self.payload = {
                "model": "gpt-3.5-turbo",
                "messages": conversation,
                "temperature": 0.5,
                "max_tokens": 500,
                "presence_penalty": 0,
                "frequency_penalty": 0,
            }

            self.headers = {"Authorization": f'Bearer {settings.GPT_KEY}'}

            async  with ctx.typing():
                async with session.post("https://api.openai.com/v1/chat/completions", json=self.payload, headers=self.headers) as resp:
                    self.response = await resp.json()
                    # embed = discord.Embed(title="Chat GPT's Response:",
                    #                     description=response['choices'][0]['message']['content'])
                    await ctx.reply(self.response['choices'][0]['message']['content'])
                    print("GPT total tokens: " + str(self.response['usage']['total_tokens']))




async def setup(bot):
    await bot.add_cog(OpenAI(bot))