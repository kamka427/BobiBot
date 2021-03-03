from discord.ext import commands
import discord
from pathlib import Path
from TikTokApi import TikTokApi
import random
import string
from random import randint
from selenium import webdriver

# Optional argument, if not specified will search path.
driver = webdriver.Chrome('chromedriver')
driver.get('http://www.google.com/')
# from selenium import webdriver
# import os

# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# driver = webdriver.Chrome(executable_path=os.environ.get(
#     "CHROMEDRIVER_PATH"), chrome_options=chrome_options)


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
        count = 50
        tiktoks = api.trending(count=count)
        Path("downloads").mkdir(exist_ok=True)
        n = 1
        for i in range(n):
            r = randint(0, 49)
            data = api.get_Video_By_TikTok(tiktoks[r])  # bytes of the video
            with open("downloads/video.mp4".format(str(r)), 'wb') as output:
                output.write(data)
        await ctx.send(file=discord.File(r'downloads/video.mp4'))

    # @commands.command(aliases=['Tik1'])
    # async def tok(self, ctx, name):
    #     did = ''.join(random.choice(string.digits) for num in range(19))
    #     verifyFp = "verify_YOUR_VERIFYFP_HERE"
    #     api = TikTokApi.get_instance(
    #         use_selenium=True, custom_verifyFp=verifyFp, custom_did=did)
    #     print(api.byUsername(name))
    #     count = 100
    #     tiktoks = api.byUsername(name, count, language='en', proxy=None)
    #     Path("downloads").mkdir(exist_ok=True)
    #     n = 1
    #     for i in range(n):
    #         r = randint(1, 99)
    #         data = api.get_Video_By_TikTok(tiktoks[r])  # bytes of the video
    #         with open("downloads/video.mp4".format(str(r)), 'wb') as output:
    #             output.write(data)
    #     await ctx.send(file=discord.File(r'downloads/video.mp4'))

    # @commands.command(aliases=['Tik2'])
    # async def tokh(self, ctx, name):
    #     did = ''.join(random.choice(string.digits) for num in range(19))
    #     verifyFp = "verify_YOUR_VERIFYFP_HERE"
    #     api = TikTokApi.get_instance(
    #         use_selenium=True, custom_verifyFp=verifyFp, custom_did=did)
    #     # print(api.byUsername(name))
    #     count = 1
    #     tiktoks = api.byHashtag(name, count, language='en', proxy=None)
    #     Path("downloads").mkdir(exist_ok=True)
    #     n = 1
    #     for i in range(n):
    #         r = 1
    #         data = api.get_Video_By_TikTok(tiktoks[r])  # bytes of the video
    #         with open("downloads/video.mp4".format(str(r)), 'wb') as output:
    #             output.write(data)
    #     await ctx.send(file=discord.File(r'downloads/video.mp4'))


def setup(bot):
    bot.add_cog(TikTok(bot))
