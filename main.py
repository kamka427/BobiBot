from dotenv import load_dotenv
import discord
import os
from discord.ext import commands
import random


load_dotenv()


bot = commands.Bot(command_prefix='&')


@bot.listen('on_message')
async def yostuff(message):
    if message.author == bot.user:
        return
    message.content = message.content.lower().replace(' ', '')
    if message.content.startswith('hello'):
        await message.channel.send('Yo!')

    if message.content.startswith('yo'):
        await message.channel.send('yo yo yo!')

    if message.content.startswith('myqueen'):
        await message.channel.send('https://www.twitch.tv/pokimane')

    if message.content.startswith('pog'):
        await message.channel.send('https://www.nme.com/wp-content/uploads/2021/01/pogchamp-twitch-696x442.jpg')

    if message.content.startswith('aqua'):
        await message.channel.send('https://media.tenor.com/images/254629658d75071285e84502d71c67c1/tenor.gif')

    if message.content.startswith('v'):
        await message.channel.send('guys v?')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)


@bot.command()
async def repeat(cont, times: int, content='Repeating...'):
    """Tobbszor megismetel egy uzenetet."""
    for i in range(times):
        await cont.send(content)


@bot.command(description='Nem tudsz valamit eldonteni?')
async def choose(cont, *choices: str):
    """Egyet valaszt a lehetosegekbol."""
    await cont.send(random.choice(choices))


@bot.command()
async def roll(cont, dice: str):
    """Rolls a dice in N*N format."""
    try:
        rolls, limit = map(int, dice.split('*'))
    except Exception:
        await cont.send('Format has to be in N*N!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await cont.send(result)

bot.run(os.getenv('TOKEN'))
