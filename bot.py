import discord
# from dotenv import load_dotenv  # !
from discord.ext import commands
import os
import asyncpraw
# load_dotenv()  # !

cogs = [
    'music', 'reddit', 'tiktok', 'messages'
]

bot = commands.Bot(command_prefix="&", description="Bobi az ezermester")
reddit = asyncpraw.Reddit(client_id=os.getenv('CLIENTID'),
                          client_secret=os.getenv('CLIENTSECRET'),
                          user_agent=os.getenv('USERAGENT'))

if __name__ == '__main__':
    for name in cogs:
        bot.load_extension("cogs.{}".format(name))
    
@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------------------------------------------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Peepo"))

bot.run(os.getenv('TOKEN'))
