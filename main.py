from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import praw
import random


load_dotenv()


bot = commands.Bot(command_prefix='&')


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

    # if message.content == 'diktator':
    #     await message.channel.send('https://cdn.discordapp.com/attachments/546393279827017729/804124792831082506/ayykos.png')

    # if "sadgest" in message.content:
    #     await message.channel.send('https://cdn.discordapp.com/attachments/546393279827017729/804124792831082506/ayykos.png')


# @bot.event
# async def on_message(message):
#     # No infinite bot loops
#     if message.author == bot.user or message.author.bot:
#         return

#     mention = message.author.mention
#     response = f"{mention}, get yo a$$ here!"
#     await message.channel.send(response)
# @bot.command(name='ping', help='Ping the bot to text name')
# async def ping(ctx):
#     # await ctx.send('Pong {0}'.format(ctx.author))
#     await ctx.send(format(ctx.author.display_name) + " get yo a$$ here!")
#     # print("debug: " + dir(ctx.author))
# @bot.command()
# async def sadgest(ctx, *, user: discord.Member = None):
#     # if user == "Sadgest":
#     await ctx.send(f"{user.mention}, get yo a$$ here! " + 'https://cdn.discordapp.com/attachments/546393279827017729/804124792831082506/ayykos.png')


@bot.command()
async def m(ctx, *, user: discord.Member = None):
    if user:
        await ctx.send(f"{user.mention}, get yo a$$ here!")
    elif user == "Sadgest":
        await ctx.send(f"{user.mention}, get yo a$$ here! " + 'https://cdn.discordapp.com/attachments/546393279827017729/804124792831082506/ayykos.png')
    else:
        await ctx.send('You have to say who needs to get his/her a$$ here!')


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


reddit = praw.Reddit(client_id=os.getenv('CLIENTID'),
                     client_secret=os.getenv('CLIENTSECRET'),
                     user_agent=os.getenv('USERAGENT'))


@bot.command()
async def hotmeme(cont):
    memes_submissions = reddit.subreddit('memes').hot()
    post_to_pick = random.randint(1, 10)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    await cont.send(submission.url)


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

bot.run(os.getenv('TOKEN'))
