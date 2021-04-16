from discord.ext import commands
import traceback
import json
import requests
import datetime

class ExceptionHandler(commands.Cog):
    """Ignore this. This cog handles errors"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        tbc = traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__)
        tbctext = ''

        for i in tbc:
            tbctext += i
        
        url = json.load(open('.\\assets\\keys.json', 'r'))['ERROR_WEBHOOK']
        timestamp = str(datetime.datetime.utcnow())
        await ctx.send('An internal error occurred! We are very sorry.\nPease DM the following to `Zukashi#7071`:')
        await ctx.send('`DPY-001_{}`'.format(timestamp))
        msg = 'DPY-001_{}\n```{}```'.format(timestamp, tbctext)
        data = {
            'content': msg
        }

        requests.post(url, data)

    @commands.command()
    async def errortest(self, ctx):
        raise Exception('valid exception')

def setup(bot):
    bot.add_cog(ExceptionHandler(bot))
