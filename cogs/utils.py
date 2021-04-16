from discord.ext import commands
from requests

class Utils(commands.Cog, name = "Utilities"):
    def __init__(self, bot):
      self.bot = bot
      # self.weather_key = os.environ['OPENWEATHER_API_KEY']
      self.weather_key = "fb9df86d9c484eba8a69269cfb0beac9"
    
    @commands.command()
    async def weather(self, ctx,  *, city):
        data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID=fb9df86d9c484eba8a69269cfb0beac9").json()
        cleared_data = {
            'City': data['name'],
            'Weather': f"{data['weather'][0]['main']} - {data['weather'][0]['description']}",
            'Temperature': f"{data['main']['temp']}°C",
            'Humidity': f"{data['main']['humidity']}%",
            'Pressure': f"{data['main']['pressure']}Pa",
            'Clouds': f"{data['clouds']['all']}%",
            'Wind': f"{data['wind']['speed']} km/h"
        }
        embed = Embed(title=f":white_sun_small_cloud: Weather in {cleared_data['City']}", color=0x3498db)
        for key, value in cleared_data.items():
            embed.add_field(name=key, value=value)
        await ctx.send(embed=embed)
   
def setup(bot):
    bot.add_cog(Utilities(bot))
