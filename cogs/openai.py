from discord.ext import commands

import openai
import aiohttp

import os


from dotenv import load_dotenv
load_dotenv()

GPT_KEY = os.getenv('GPT_API_KEY')
openai.api_key = GPT_KEY


class OpenAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(help="GPT 3.5 Turbo")
    async def chat(self, ctx: commands.Context, *, prompt: str):

        if ctx.channel.id != 1092256153968332800:
            await ctx.reply("Must be in gpt_bot")
            return
        async with aiohttp.ClientSession() as session:

            self.conversation = [{"role": "system", "content": "I am a friendly chatbot"}]           
            
            self.prev_message = []
            async for msg in ctx.channel.history(limit=15):
                if msg.content.startswith("!GPT ") == True and msg.author.id == ctx.author.id:
                    self.prev_message.append({'role': 'user', 'content': msg.content[5:]})
            self.prev_message.reverse()
            for message in self.prev_message:
                self.conversation.append(message)
        

            self.payload = {
                "model": "gpt-3.5-turbo",
                "messages": self.conversation,
                "temperature": 0.5,
                "max_tokens": 500,
                "presence_penalty": 0,
                "frequency_penalty": 0,
            }



            self.headers = {"Authorization": f'Bearer {GPT_KEY}'}

            async  with ctx.typing():
                async with session.post("https://api.openai.com/v1/chat/completions", json=self.payload, headers=self.headers) as resp:
                    self.response = await resp.json()
                    # embed = discord.Embed(title="Chat GPT's Response:",
                    #                     description=response['choices'][0]['message']['content'])
                    await ctx.reply(self.response['choices'][0]['message']['content'])
                    print("GPT total tokens: " + str(self.response['usage']['total_tokens']))


    @commands.command(help="Get AI Generated image (1024*1024)")
    async def GPTImage(self, ctx:commands.Context, *, prompt: str):
        
        async with aiohttp.ClientSession() as session:
            
            async  with ctx.typing():
                response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024"
                )
                image_url = response['data'][0]['url']

                await ctx.reply(image_url)




    @commands.command(help="Davinci 3")
    async def Davinci(self, ctx: commands.Context, *, prompt: str):
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
                async with ctx.typing():
                    self.response = await resp.json()
                    # embed = discord.Embed(title="Chat GPT's Response:",
                    #                     description=response["choices"][0]["text"])
                await ctx.reply(self.response["choices"][0]["text"])


async def setup(bot):
    await bot.add_cog(OpenAI(bot))