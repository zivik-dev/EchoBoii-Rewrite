from discord.ext import commands
import requests
import os
import re
from urllib.parse import quote as urlfix

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

class Utils(commands.Cog, name = "Utilities"):
    def __init__(self, bot):
      self.bot = bot
      self.weather_key = os.environ['OPENWEATHER_API_KEY']
    
    @commands.command(name="Weather", aliases = ['weather'], brief = "Get current weather of city", description = "This command gets weather of the city passed on it. May or may not be accurate.")
    async def weather(self, ctx,  *, city):
        data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={self.weather_key}").json()
        
        sorted_data = {
            'City': data['name'],
            'Weather': f"{data['weather'][0]['main']} - {data['weather'][0]['description']}",
            'Temperature': f"{data['main']['temp']}°C",
            'Humidity': f"{data['main']['humidity']}%",
            'Pressure': f"{data['main']['pressure']}Pa",
            'Clouds': f"{data['clouds']['all']}%",
            'Wind': f"{data['wind']['speed']} km/h"
        }
        
        embed = Embed(title=f":white_sun_small_cloud: Weather in {sorted_data['City']}", color=0x3498db)
                      
        for key, value in sorted_data.items():
            embed.add_field(name=key, value=value)
                      
        await ctx.send(embed=embed)

    @commands.command(name="Wikipedia", aliases=['wiki', 'wikipedia'], brief="Get summary of a wikipedia article", description="This commands gets summary of a topic from a wikipedia article. Usage: eb wiki Bruno Mars")
    async def wikipedia(self, ctx, *, query):
        data = requests.get('https://en.wikipedia.org/wiki/{}'.format(urlfix(query)))
        if data.status_code != 200:
            await ctx.send('Sorry, could not find any data.\nDetails: `STATUS_CODE != 200')
        else:
            await ctx.send(cleanhtml(data.text.split('<p>')[1]))
   
def setup(bot):
    bot.add_cog(Utilities(bot))
