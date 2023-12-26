import discord
from discord import app_commands
import aiohttp

import settings
WEATHER_API_KEY = settings.WEATHER_API_KEY



def date_swap(dates_list):
    dates = dates_list.split("-")
    dates[0], dates[1], dates[2] = dates[1], dates[2], dates[0]
    return "-".join(dates)


class Weather(app_commands.Group):

    @app_commands.command(description="Returns temperature (F) in city provided")
    async def temperature(self, interaction: discord.Interaction, location:str = "New York"):
        
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}"

        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            api_url=url
            async with session.get(api_url) as resp:
                try:
                    data = await resp.json()
                    response = f"{data['location']['name']}: {data['current']['temp_f']}°F"
                    await interaction.followup.send(response)
                except:
                    await interaction.followup.send(f"Location ({location}) data unavailable")

    @app_commands.command(description="Returns forecasted temperatures for up to 3 days (including today)")
    async def forecast(self, interaction: discord.Interaction, location:str = "New York", days:int = 1):
        if days > 3:
            days = 3
        elif days < 1:
            days = 1
            
        url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days={days}"

        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            api_url=url
            async with session.get(api_url) as resp:
                try:
                    data = await resp.json()
                    response = f"##  {data['location']['name']}  ##\n"
                    for day in data['forecast']['forecastday']:
                        response += date_swap(day['date']) + "\n"
                        response += f"   High: {day['day']['maxtemp_f']}°F\n"
                        response += f"   Low: {day['day']['mintemp_f']}°F\n\n"

                    await interaction.followup.send(response)


                except Exception as error:
                    print(error)
                    await interaction.followup.send(f"Location ({location}) data unavailable")
                    

async def setup(bot):
    bot.tree.add_command(Weather(name="weather", description="Get Temperature data"))