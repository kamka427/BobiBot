from discord.utils import get
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import praw
import random
import youtube_dl
import asyncio

load_dotenv()


bot = commands.Bot(command_prefix='&')

reddit = praw.Reddit(client_id=os.getenv('CLIENTID'),
                     client_secret=os.getenv('CLIENTSECRET'),
                     user_agent=os.getenv('USERAGENT'))

players = {}


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Peepo"))


@bot.listen('on_message')
async def yostuff(message, user: discord.Member = None):
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

    if message.content.startswith('rahim'):
        await message.channel.send('https://cdn.discordapp.com/attachments/546393279827017729/804093858005647400/Cd7DPJqWEAEcRm9.jpg')

    if message.content == 'diktator':
        await message.channel.send('https://cdn.discordapp.com/attachments/546393279827017729/804124792831082506/ayykos.png')

    if "sadgest" in message.content:
        await message.channel.send('https://cdn.discordapp.com/attachments/546393279827017729/804124792831082506/ayykos.png')

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


@bot.command()
async def m(ctx, *, user: discord.Member = None):
    if user:
        await ctx.send(f"{user.mention}, get yo a$$ here!")
    elif user == "Sadgest":
        await ctx.send(f"{user.mention}, get yo a$$ here! " + 'https://cdn.discordapp.com/attachments/546393279827017729/804124792831082506/ayykos.png')
    else:
        await ctx.send('You have to say who needs to get his/her a$$ here!')


@bot.command()
async def repeat(ctx, times: int, content='Repeating...'):
    """Tobbszor megismetel egy uzenetet."""
    for i in range(times):
        await ctx.send(content)


@bot.command(description='Nem tudsz valamit eldonteni?')
async def choose(ctx, *choices: str):
    """Egyet valaszt a lehetosegekbol."""
    await ctx.send(random.choice(choices))


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in N*N format."""
    try:
        rolls, limit = map(int, dice.split('*'))
    except Exception:
        await ctx.send('Format has to be in N*N!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command()
async def hotmeme(ctx):
    memes_submissions = reddit.subreddit('memes').hot()
    post_to_pick = random.randint(1, 10)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    await ctx.send(submission.url)


@bot.command(aliases=['Meme'])
async def meme(ctx):
    submission = reddit.subreddit("memes").random()
    await ctx.send(submission.url)


@bot.command(aliases=['Saber'])
async def saber(ctx):
    submission = reddit.subreddit("saber").random()
    await ctx.send(submission.url)


@bot.command(aliases=['Trap'])
async def trap(ctx):
    submission = reddit.subreddit("astolfo").random()
    await ctx.send(submission.url)


@bot.command(aliases=['Peepo'])
async def peepo(ctx):
    submission = reddit.subreddit("peepos").random()
    await ctx.send(submission.url)


@bot.command(aliases=['Reddit'])
async def r(ctx, name):
    submission = reddit.subreddit(name).random()
    await ctx.send(submission.url)


@bot.command()
async def play(ctx, *, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels)
    await voiceChannel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'default_search': 'auto',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        await ctx.send(f'**Playing: **{url}')
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

    while voiceChannel.is_playing():
        await asyncio.sleep(1)
    else:
        await voiceChannel.disconnect()
        print("Disconnected")


@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    await voice.disconnect()
    print("Disconnected")

bot.run(os.getenv('TOKEN'))
