from discord.ext import commands
from requests
import os

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
   
def setup(bot):
    bot.add_cog(Utilities(bot))
