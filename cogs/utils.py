from discord.ext import commands
import requests
import os
import re
import lxml.html as htm
from urllib.parse import quote as urlfix
from googletrans import Translator
from langcodes import Language

translator = Translator()

def cleanBraces(rtext):
  return re.sub(r"\[[^[]]*\]", "", rtext) # HAHAHAHAH GOT IT, GET REKT

class Utils(commands.Cog, name = "Utilities"):
"""Useful utilities. The best of EchoBoii!!"""
    def __init__(self, bot):
      self.bot = bot
      self.weather_key = os.environ['OPENWEATHER_API_KEY']
    
    @commands.command(name="weather", aliases = ['weather'], brief = "Get current weather of city", description = "This command gets weather of the city passed on it. May or may not be accurate.")
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

    @commands.command(name="wikipedia", aliases=['wiki', 'wikipedia'], brief="Get summary of a wikipedia article", description="This commands gets summary of a topic from a wikipedia article. Usage: eb wiki Bruno Mars")
    async def wikipedia(self, ctx, *, query):
        data = requests.get('https://en.wikipedia.org/wiki/{}'.format(urlfix(query)))
        if data.status_code != 200:
            await ctx.send('Sorry, could not find any data. Try removing any extra spaces or an \'s\'.\nExample: Type \'fruit\' instead of \'fruits\'\nDetails: `STATUS_CODE != 200')
        else:
            await ctx.send(cleanBraces(htm.fromstring(data.text.split('<p>')[1].split('</p>')[0]).text_content()))

    @commands.command(name="translate", aliases=['gtrans', 'translate'], brief='Translate text to a wide variety of languages.', description='This command translates text to another specified language. Please use language codes like \'en\'/\'fr\'')
    async def gtrans(self, ctx, langcode, *, text):
        tobj = translator.translate(text, dest=langcode)
        srcl = Language.make(language=tobj.src).display_name()
        await ctx.send('**__Original Text:__** {}\n**__Translated Text:__** {}\n**__Pronounciation:__** {}\n**__Source Language:__** {}'.format(text, tobj.text, tobj.pronunciation, srcl))
   
def setup(bot):
    bot.add_cog(Utils(bot))
