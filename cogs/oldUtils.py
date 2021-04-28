from discord.ext import commands
import discord
import requests
import random
import os
from urllib.parse import quote as urlfix

class OldCommands(commands.Cog, name='Old Utilities'):
    """commands copy-pasted from legacy version because they were already perfect (pls dont hate us for this lmao)"""
    def __init__(self, bot):
        self.bot = bot
        self.weather_key = os.environ['OPENWEATHER_API_KEY']
    
    @commands.command(name='whois', brief='Get information about a user', description='Get information of a user by pinging them. Not passing any ping will show your own information.')
    async def whois(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        embed = discord.Embed(
        title = 'User Information',
        description = f'User Information for {member.display_name}',
        colour = member.color
        )

        embed.set_thumbnail(url = member.avatar_url)
    
        embed.add_field(name = "Name:", value = member, inline = False)
        embed.add_field(name = "ID:", value = member.id, inline = False)
        embed.add_field(name = "Server:", value = member.guild, inline = False)
        embed.add_field(name = "Account Creation On:", value = member.created_at.strftime('%a %#d %B %Y, %I:%M %p UTC'), inline = False)
        embed.add_field(name = "Joined This Server On:", value = member.joined_at.strftime('%a %#d %B %Y, %I:%M %p UTC'), inline = False)
        embed.add_field(name = "Top Role:", value = member.top_role.mention, inline = False)
        embed.add_field(name = "Current Activity/Status:", value = member.activity, inline = False)
        embed.add_field(name = "Is A Bot?:", value = member.bot, inline = False)

        await ctx.send(embed = embed)

    @commands.command(name='sinfo', brief='Get server information.', description='Gets the current server\'s data')
    async def sinfo(self, ctx):

        server = ctx.author.guild
        embed = discord.Embed(
        title = 'Server Information',
        description = f'Server Information for {server.name}',
        colour = server.owner.colour
        )

        embed.set_thumbnail(url = server.icon_url)
    
        embed.add_field(name = "Name:", value = server.name, inline = False)
        embed.add_field(name = "ID:", value = server.id, inline = False)
        embed.add_field(name = "Region:", value = server.region, inline = False)
        embed.add_field(name = "Owner:", value = server.owner, inline = False)
        embed.add_field(name = "Member Count:", value = server.member_count, inline = False)
        embed.add_field(name = "Created At:", value = server.created_at.strftime('%a %#d %B %Y, %I:%M %p UTC'), inline = False)
        embed.add_field(name = "Verification Level:", value = server.verification_level, inline = False)
        embed.add_field(name = "Text Channels:", value = len(server.text_channels), inline = False)
        embed.add_field(name = "Voice Channels:", value = len(server.voice_channels), inline = False)   
        embed.add_field(name = "Emojis:", value = len(server.emojis), inline = False) 

        await ctx.send(embed = embed)

    @commands.command(name="weather", aliases = ['weather'], brief = "Get current weather of city", description = "This command gets weather of the city passed on it. May or may not be accurate.")
    async def weather(self, ctx,  *, city):
        data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={urlfix(city)}&units=metric&APPID={self.weather_key}").json()
        
        sorted_data = {
            'City': data['name'],
            'Weather': f"{data['weather'][0]['main']} - {data['weather'][0]['description']}",
            'Temperature': f"{data['main']['temp']}°C",
            'Humidity': f"{data['main']['humidity']}%",
            'Pressure': f"{data['main']['pressure']}Pa",
            'Clouds': f"{data['clouds']['all']}%",
            'Wind': f"{data['wind']['speed']} km/h"
        }
        
        embed = discord.Embed(title=f":white_sun_small_cloud: Weather in {sorted_data['City']}", color=0x3498db)
                      
        for key, value in sorted_data.items():
            embed.add_field(name=key, value=value)
                      
        await ctx.send(embed=embed)

    @commands.command(aliases = ['8ball'], brief='Ask a question!', description='Ask the bot a question and it will reply you to it. WARNING: There\'s no need to judge your life with this because its just a simple game that can output anything randomly. Just use for fun.')
    async def _8ball(self, ctx, *, question):
        answers = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
        ]

        embed = discord.Embed(
        title = "8ball",
        colour = ctx.author.colour
        )

        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        embed.add_field(name = f"Question: **{question}**", value = f"Answer: **{random.choice(answers)}**")

        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(OldCommands(bot))
