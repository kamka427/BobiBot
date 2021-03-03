from discord.ext import commands
import discord
from pathlib import Path
from TikTokApi import TikTokApi
import random
import string
from random import randint
from selenium.webdriver import Chrome
from selenium import webdriver
import os

op = webdriver.ChromeOptions()
op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
op.add_argument('--headless')
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-sh-usage")
driver = webdriver.Chrome(
    executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)


class TikTok(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Tik'])
    async def tik(self, ctx):
        did = ''.join(random.choice(string.digits) for num in range(19))
        verifyFp = "verify_YOUR_VERIFYFP_HERE"
        api = TikTokApi.get_instance(
            use_selenium=True, custom_verifyFp=verifyFp, custom_did=did)
        # print(api.trending())
        count = 100
        tiktoks = api.trending(count=count)
        Path("downloads").mkdir(exist_ok=True)
        n = 1
        for i in range(n):
            r = randint(1, 99)
            data = api.get_Video_By_TikTok(tiktoks[r])  # bytes of the video
            with open("downloads/video.mp4".format(str(r)), 'wb') as output:
                output.write(data)
        await ctx.send(file=discord.File(r'downloads/video.mp4'))

    @commands.command(aliases=['Tik1'])
    async def tok(self, ctx, name):
        did = ''.join(random.choice(string.digits) for num in range(19))
        verifyFp = "verify_YOUR_VERIFYFP_HERE"
        api = TikTokApi.get_instance(
            use_selenium=True, custom_verifyFp=verifyFp, custom_did=did)
        print(api.byUsername(name))
        count = 100
        tiktoks = api.byUsername(name, count, language='en', proxy=None)
        Path("downloads").mkdir(exist_ok=True)
        n = 1
        for i in range(n):
            r = randint(1, 99)
            data = api.get_Video_By_TikTok(tiktoks[r])  # bytes of the video
            with open("downloads/video.mp4".format(str(r)), 'wb') as output:
                output.write(data)
        await ctx.send(file=discord.File(r'downloads/video.mp4'))

    @commands.command(aliases=['Tik2'])
    async def tokh(self, ctx, name):
        did = ''.join(random.choice(string.digits) for num in range(19))
        verifyFp = "verify_YOUR_VERIFYFP_HERE"
        api = TikTokApi.get_instance(
            use_selenium=True, custom_verifyFp=verifyFp, custom_did=did)
        # print(api.byUsername(name))
        count = 1
        tiktoks = api.byHashtag(name, count, language='en', proxy=None)
        Path("downloads").mkdir(exist_ok=True)
        n = 1
        for i in range(n):
            r = 1
            data = api.get_Video_By_TikTok(tiktoks[r])  # bytes of the video
            with open("downloads/video.mp4".format(str(r)), 'wb') as output:
                output.write(data)
        await ctx.send(file=discord.File(r'downloads/video.mp4'))


def setup(bot):
    bot.add_cog(TikTok(bot))
