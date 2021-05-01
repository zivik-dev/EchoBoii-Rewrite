import discord
from discord.ext import commands
import datetime
import time

start_time = time.time()

class Misc(commands.Cog, name='Misc'):
    """Misc Commands, mostly for development use."""
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def about(self, ctx):
    #     about_bot = "Hello from EchoBoii!\n---------------------\nThis is a discord bot made for fun games and utility commands.\n---------------------\nThe bot was created and being managed by jailbreak.exe#7071 using Python3's discord.py library\nPlease DM jailbreak.exe#7071 if there are any bugs"
    #     await ctx.send(f"```{about_bot}```")

    @commands.command(name='status', brief='Bot\'s Status', description='Get bot\'s status like ping, uptime etc.')
    async def status(self, ctx):
        bot_ping = int(self.bot.latency * 1000)
        bot_servers = len(self.bot.guilds)
        bot_stz = "UTC"
        current_time = time.time()
        difference = int(round(current_time - start_time))
        uptime = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(title = "Bot Status!", colour = self.bot.user.colour)

        embed.set_thumbnail(url = self.bot.user.avatar_url)

        embed.add_field(name = "Bot's Ping:", value = bot_ping, inline = False)
        embed.add_field(name = "Standard TimeZone:", value = bot_stz, inline = False)
        embed.add_field(name = "Server Count:", value = bot_servers, inline = False)
        embed.add_field(name = "Bot's Uptime:", value = uptime, inline = False)

        await ctx.send(embed = embed)
        
def setup(bot):
  bot.add_cog(Misc(bot))
