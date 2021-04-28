from discord.ext import commands

class MostUsed(commands.Cog, name="Most Used"):
    """Most used commands of EchoBoii of all time! Even more improved!!"""

    def __init__(self, bot):
        self.bot = bot
        self.spamFlag = False

    @commands.command(name='spam', brief='Spam without hassle!!', description='This command spams text/images with one command. WARNING: To avoid spamming on main channels, the spam channel must contain the word \'spam\' in it, or the command will fail.')
    async def spam(self, ctx, numberOftimes, content):
        try:
            int(numberOftimes)
        except:
            await ctx.send('Pass a number at the place of the \'numberOftimes\' variable. See help for more information.')

        if '@everyone' in str(content):
            await ctx.send("`@everyone` spam ping not allowed")
            return

        if '@' in str(content):
            await ctx.send('Sorry, You can\'t put \'@\' in your message. This is to avoid spam pings')
            return

        if 'spam' not in (ctx.channel.name).lower():
            await ctx.send('The channel\'s name doesn\'t contain the word \'spam\' in it.')
            return

        if int(numberOftimes) > 100:
            await ctx.send('Only 100 messages/images spam at a time!')
            return

        for i in range(int(numberOftimes)):
            if not self.spamFlag:
                await ctx.send(content)
            else:
                await ctx.send('Spam has been stopped!!')
                self.spamFlag = False
                break

    @commands.command(name='spamStop', brief='Stop a running spam.', description='This command stops a running spam. WARNING: This command is currently unstable and will stop any spam in any server. So consider not using it if not important. (PS: We\'re still trying to find a better way to spam)')
    async def spamStop(self, ctx):
        self.spamFlag = True

def setup(bot):
    bot.add_cog(MostUsed(bot))
