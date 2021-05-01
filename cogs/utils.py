from discord.ext import commands
import requests
import os
import re
import lxml.html as htm
from urllib.parse import quote as urlfix
from googletrans import Translator
from langcodes import *
import discord
import datetime, pytz
from pytz.exceptions import UnknownTimeZoneError as UTZE
import time

def convert24(str1):
    if str1[-2:] == "AM" and str1[:2] == "12":
        return "00" + str1[2:-2]
  
    elif str1[-2:] == "AM":
        return str1[:-2]

    elif str1[-2:] == "PM" and str1[:2] == "12":
        return str1[:-2]
          
    else:
        return str(int(str1[:2]) + 12) + str1[2:8]

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

    @commands.command(name="translate", aliases=['gtrans'], brief='Translate text to a wide variety of languages.', description='This command translates text to another language. Usage: eb translate en jus de chocolat (Output -> Chocolate Juice)')
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
        
        await ctx.send('Message Sent :white_check_mark:')

    # UNDER DEVELOPENT, DOESNT WORK YET
    @commands.command(name='timein', brief='Get your time in some other timezone!!', description='This command will convert a given time of your timezone to another specified timezone. Supports both 12-hour time and 24-hour time input. Outputs 24-hour time. Only accepts timezone regions like \'Asia/Kolkata\' as parameters. Formats like \'EST\' or \'IST\' are not allowed!')
    async def timein(self, ctx, your_tz, convert_time, convertTo_tz):
        local_time = convert_time
        local_tz = your_tz
        convert_tz = convertTo_tz

        await ctx.send('Converting . . . /')

        ltstemp = local_time.split(':')
        ltstemp = [ltstemp[0], ltstemp[1].replace('AM', '').replace('PM', '')]
        t1s, t2s = local_time.split(':')[0], local_time.split(':')[1]
        if len(ltstemp[0]) != 2:
            t1s = '0' + ltstemp[0]
        if len(ltstemp[1]) != 2:
            t2s = '0' + ltstemp[1]
        newstr = t1s + ':' + t2s

        if 'PM' in local_time.upper():
            newstr += ' PM'
        if 'AM' in local_time.upper():
            newstr += 'AM'

        local_time = newstr

        del ltstemp, newstr, t1s, t2s

        if 'PM' in local_time.upper():
            meridien = local_time.split(' ')[1].strip()
            time = local_time.split(' ')[0].split(':')
            local_time = convert24(f'{time[0]}:{time[1]}:00 {meridien}')

        if 'AM' in local_time.upper():
            meridien = local_time.split(' ')[1].strip()
            time = local_time.split(' ')[0].split(':')
            local_time = convert24(f'{time[0]}:{time[1]}:00 {meridien}')

        local_time = local_time.split(':')

        try:
            local_pytz = pytz.timezone(local_tz)
        except UTZE:
            await ctx.send('Timezones should be in the following format:\n`Asia/Kolkata`\nPlease avoid using format like:\n`IST` or `CEST`')

        utcnow = datetime.datetime.utcnow()
        timestr = f'{utcnow.year}-{utcnow.month}-{utcnow.day} {local_time[0]}:{local_time[1]}:{utcnow.second}.{utcnow.microsecond}'
        datetime_tobj = datetime.datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S.%f')

        try:
            converted_dtobj = datetime_tobj.astimezone(pytz.timezone(convert_tz))
        except UTZE:
            await ctx.send('Timezones should be in the following format:\n`Asia/Kolkata`\nPlease avoid using format like:\n`IST` or `CEST`')

        await ctx.send('**Converted Time:** {}:{}'.format(converted_dtobj.hour, converted_dtobj.minute))

   
def setup(bot):
    bot.add_cog(Utils(bot))
