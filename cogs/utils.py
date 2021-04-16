from discord.ext import commands

class Utils(commands.Cog, name = "Utilities"):
  def __init__(self, bot):
    self.bot = bot
    
  def weather(self, ctx, *, city):
    
   
def setup(bot):
  bot.add_cog(Utilities(bot))
