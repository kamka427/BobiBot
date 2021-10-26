import asyncpraw
from discord.ext import commands
import os
import random
allow_requests = True

reddit = asyncpraw.Reddit(client_id=os.getenv('CLIENTID'),
                          client_secret=os.getenv('CLIENTSECRET'),
                          user_agent=os.getenv('USERAGENT'))


class Reddit(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def hotmeme(self, ctx):
        subreddit = await reddit.subreddit("memes")
        memes_submissions = await subreddit.hot()
        post_to_pick = random.randint(1, 10)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.    stickied)
    
        await ctx.send(submission.url)
    
    @commands.command(aliases=['Meme'])
    async def meme(self, ctx):
        subreddit = await reddit.subreddit("memes")
        submission = await subreddit.random()
        await ctx.send(submission.url)
    
    @commands.command(aliases=['Saber'])
    async def saber(self, ctx):
        subreddit = await reddit.subreddit("saber")
        submission = await subreddit.random()
        await ctx.send(submission.url)
    
    @commands.command(aliases=['Waifu'])
    async def waifu(self, ctx):
        subreddit = await reddit.subreddit("saber")
        submission = await subreddit.random()
        m = await ctx.send(submission.url)
        await m.add_reaction("❤")
        await ctx.send("She is a " + str(random.randint(1, 5)) + " star waifu!")
    
    @commands.command(aliases=['Trap'])
    async def trap(self, ctx):
        subreddit = await reddit.subreddit("astolfo")
        submission = await subreddit.random()
        await ctx.send(submission.url)
     
    @commands.command(aliases=['Peepo'])
    async def peepo(self, ctx):
        subreddit = await reddit.subreddit("peepo")
        submission = await subreddit.random()
        await ctx.send(submission.url)
    
    @commands.command(aliases=['Movie'])
    async def movie(self, ctx):
        subreddit = await reddit.subreddit("trailers")
        submission = await subreddit.random()
        await ctx.send(submission.url)

    @commands.command(aliases=['Egirl'])
    async def egirl(self, ctx):
        subreddit = await reddit.subreddit("egirl")
        submission = await subreddit.random()
        await ctx.send(submission.url)
    
    @commands.command(aliases=['Reddit'])
    async def r(self, ctx, name):
        subreddit = await reddit.subreddit(name)
        submission = await subreddit.random()
        await ctx.send(submission.url)
    
def setup(bot):
    bot.add_cog(Reddit(bot))
