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
                print(response_string)
                await interaction.followup.send(response_string)
            except requests.RequestException as e:
                await interaction.followup.send(f"Error: Server probably asleep")

    # @app_commands.command(description="Get AI Generated image")
    # async def image(self, interaction: discord.Interaction, img_prompt: str):
    #     await interaction.response.defer()

    #     async with aiohttp.ClientSession() as session:
    #         url = "https://api.limewire.com/api/image/generation"
    #         header = {"Content-Type": "application/json",
    #                   "X-Api-Version": "v1",
    #                   "Accept": "application/json",
    #                   "Authorization": f"Bearer {LIMEWIRE_KEY}"}

    #         payload = payload = {"prompt": img_prompt,
    #                              "aspect_ratio": "1:1"}

    #         r = requests.post(url=url, json=payload, headers=header)
    #         if r.status_code == 200:
    #             data = r.json()

    #             print(f"Credits remaining: {data['credits_remaining']}")
    #             await interaction.followup.send(data['data'][0]['asset_url'])
    #         else:
    #             await interaction.followup.send("Out of credits")

    # @app_commands.command(description="mixtral-8x7b-32768")
    # async def chat(self, interaction: discord.Interaction, prompt: str):
    #     await interaction.response.defer()
    #     async with aiohttp.ClientSession() as session:
    #         try:
    #             client = groq.Client(api_key=settings.GROQ_KEY)
    #             self.result = client.chat.completions.create(
    #                 messages=[{
    #                     "role": "user",
    #                     "content": prompt,
    #                 }
    #                 ],
    #                 model="mixtral-8x7b-32768",
    #             )
    #             print(f"Total tokens used: {self.result.usage.total_tokens}")
    #             await interaction.followup.send(self.result.choices[0].message.content)
    #         except Exception as e:
    #             print(e)


async def setup(bot):
    bot.tree.add_command(AI(name="ai", description="AI commands"))
