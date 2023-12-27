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

    # @app_commands.command(description="Returns temperature (F) in city provided")
    # async def temperature(self, interaction: discord.Interaction, location:str = "New York"):
        
    #     url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}"

    #     await interaction.response.defer()
    #     async with aiohttp.ClientSession() as session:
    #         api_url=url
    #         async with session.get(api_url) as resp:
    #             try:
    #                 data = await resp.json()
    #                 response = f"{data['location']['name']}: {data['current']['temp_f']}°F"
    #                 await interaction.followup.send(response)
    #             except:
    #                 await interaction.followup.send(f"Location ({location}) data unavailable")



    @app_commands.command(description="Returns current temperature and forecasted weather for 3 days")
    async def weather(self, interaction: discord.Interaction, location:str = "New York"):
            
        url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days=3"

        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            api_url=url
            async with session.get(api_url) as resp:
                try:
                    data = await resp.json()

                    embed = discord.Embed(
                        title=f"Weather for {data['location']['name']}, {data['location']['region']}",
                          url="https://github.com/normthenord/Discord_Bot")
                    

                    embed.add_field(
                        name=f"__Current Temperature__",
                        value=f"`{data['current']['temp_f']}°F`",
                        inline=False
                    )

                    for day in data['forecast']['forecastday']:
                        embed.add_field(
                            name=f"__{date_swap(day['date'])}__",
                            value=f"**HIGH** `{day['day']['maxtemp_f']}°F`\n**LOW** `{day['day']['mintemp_f']}°F`"
                        )
                    embed.set_thumbnail(url="https://cdn.weatherapi.com/weather/64x64/day/302.png")
                    embed.set_footer(icon_url="https://cdn.weatherapi.com/v4/images/weatherapi_logo.png", text="Courtesy of Weather API", )
                    
                    await interaction.followup.send(embed=embed)


                except Exception as error:
                    print(error)
                    await interaction.followup.send(f"Location ({location}) data unavailable")
                    

async def setup(bot):
    bot.tree.add_command(Weather(name="weather", description="Get Temperature data"))


# const embed = new EmbedBuilder()
#   .setTitle("Weather for Detroit, MI")
#   .setURL("https://github.com/normthenord/Discord_Bot")
#   .addFields(
#     {
#       name: "12-26-2023",
#       value: "**High** `65`\n**Low ** `45`",
#       inline: true
#     },
#     {
#       name: "12-27-2023",
#       value: "**High** `65`\n**Low ** `44`",
#       inline: true
#     },
#     {
#       name: "12-28-2023",
#       value: "**High**  `65`\n**Low **`45`",
#       inline: true
#     },
#   )
#   .setThumbnail("//cdn.weatherapi.com/weather/64x64/day/302.png")
#   .setColor("#00b0f4")
#   .setFooter({
#     text: "Courtesy of Weather API",
#   })
#   .setTimestamp();

# await message.reply({ embeds: [embed] });