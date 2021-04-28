from discord.ext import commands
import requests
import os
import re
import lxml.html as htm
from urllib.parse import quote as urlfix
from googletrans import Translator
from langcodes import *
import discord
import datetime

translator = Translator()

def cleanBraces(rtext):
  return re.sub(r"\[[^[]]*\]", "", rtext) # HAHAHAHAH GOT IT, GET REKT

class Utils(commands.Cog, name = "Utilities"):
    """Utility commands, most of them are from legacy version but rewritten for better output."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Wikipedia", aliases=['wiki', 'wikipedia'], brief="Get summary of a wikipedia article", description="This commands gets summary of a topic from a wikipedia article. Usage: eb wiki Bruno Mars")
    async def wikipedia(self, ctx, *, query):
        data = requests.get('https://en.wikipedia.org/wiki/{}'.format(urlfix(query)))
        if data.status_code != 200:
            await ctx.send('Sorry, could not find any data. Try removing any extra spaces or an \'s\'.\nExample: Type \'fruit\' instead of \'fruits\'\nDetails: `STATUS_CODE != 200')
        else:
            await ctx.send(cleanBraces(htm.fromstring(data.text.split('<p>')[1].split('</p>')[0]).text_content()))

    @commands.command(name="Google Translate", aliases=['gtrans', 'translate'], brief='Translate text to a wide variety of languages.', description='This command translates text to another language. Usage: eb translate en jus de chocolat (Output -> Chocolate Juice)')
    async def gtrans(self, ctx, langcode, *, text):
        tobj = translator.translate(text, dest=langcode)
        srcl = Language.make(language=tobj.src).display_name()
        await ctx.send('**__Original Text:__** {}\n**__Translated Text:__** {}\n**__Pronounciation:__** {}\n**__Source Language:__** {}'.format(text, tobj.text, tobj.pronunciation, srcl))

    @commands.command(name='suggest', brief='Suggest something for the bot', description='This command sends us (the developers) a message. So you can give us a suggestion. Example: a suggestion to bring back a command from the legacy version of the bot.')
    async def suggest(self, ctx, *, msg):
        url = os.environ['WEBHOOK_URL']
        timestamp = str(datetime.datetime.utcnow())
        msg = 'DPY-001_{} (SUGESSTION MESSAGE)\n```{}```'.format(timestamp, msg)
        data = {
            'content': msg
        }

        requests.post(url, data)
   
def setup(bot):
    bot.add_cog(Utils(bot))
