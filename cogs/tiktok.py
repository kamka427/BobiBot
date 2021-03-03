import os
from discord.ext import commands
import discord
from pathlib import Path
# from TikTokApi import TikTokApi

from random import randint
from pprint import pprint
from TikTokAPI import TikTokAPI
import nest_asyncio
# nest_asyncio.apply()

# from selenium import webdriver

# # Optional argument, if not specified will search path.
# # driver = webdriver.Chrome('cogs/chromedriver')
# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# driver = webdriver.Chrome('cogs/chromedriver', chrome_options = chrome_options)
# driver.get('http://www.google.com/')

cookie = {
    "s_v_web_id": "verify_kltdntjh_MNLKwitV_SlfJ_4x5i_9r5I_2DT9zX1QB3En",
    "tt_webid": "6928829549413320197"
}

api = TikTokAPI(cookie=cookie)


class TikTok(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Tik'])
    async def tik(self, ctx, name):
        nest_asyncio.apply()
        user = api.getVideosByUserName(name, count=10)
        video = user['items'][randint(0, 9)]['video']['id']
        api.downloadVideoById(
            video, './downloads/{}.mp4'.format((str("v"))))
        await ctx.send(file=discord.File('./downloads/v.mp4'))

    @commands.command(aliases=['Tok'])
    async def tok(self, ctx, name):
        nest_asyncio.apply()
        user = api.getVideosByHashTag(name, count=10)
        video = user['itemList'][randint(0, 9)]['video']['id']
        api.downloadVideoById(
            video, './downloads/{}.mp4'.format((str("v"))))
        await ctx.send(file=discord.File('./downloads/v.mp4'))
#     def download():
#         did = ''.join(random.choice(string.digits) for num in range(19))
#         verifyFp = "verify_YOUR_VERIFYFP_HERE"
#         api = TikTokApi.get_instance(custom_verifyFp=verifyFp, custom_did=did)
# # print(api.trending())
#         count = 50
#         tiktoks = api.trending(count=count)
#         Path("downloads").mkdir(exist_ok=True)
#         n = 50
#         for i in range(n):
#             data = api.get_Video_By_TikTok(tiktoks[i])  # bytes of the video
#             with open("downloads/{}.mp4".format(str(i)), 'wb') as output:
#                 output.write(data)

#     def __init__(self, bot):
#         self.bot = bot

#     @commands.command(aliases=['Tik'])
#     async def tik(self, ctx):
#         loop = asyncio.get_event_loop()
#         loop.run_in_executor(None, TikTok.download())
#         video = os.listdir('./downloads')
#         # Selects a random element from the list
#         videoString = random.choice(video)
#         path = "./downloads/" + videoString
#         await ctx.send(file=discord.File(path))

#     # @commands.command(aliases=['Tik1'])
#     # async def tok(self, ctx, name):
#     #     did = ''.join(random.choice(string.digits) for num in range(19))
#     #     verifyFp = "verify_YOUR_VERIFYFP_HERE"
#     #     api = TikTokApi.get_instance(
#     #         use_selenium=True, custom_verifyFp=verifyFp, custom_did=did)
#     #     print(api.byUsername(name))
#     #     count = 100
#     #     tiktoks = api.byUsername(name, count, language='en', proxy=None)
#     #     Path("downloads").mkdir(exist_ok=True)
#     #     n = 1
#     #     for i in range(n):
#     #         r = randint(1, 99)
#     #         data = api.get_Video_By_TikTok(tiktoks[r])  # bytes of the video
#     #         with open("downloads/video.mp4".format(str(r)), 'wb') as output:
#     #             output.write(data)
#     #     await ctx.send(file=discord.File(r'downloads/video.mp4'))

#     # @commands.command(aliases=['Tik2'])
#     # async def tokh(self, ctx, name):
#     #     did = ''.join(random.choice(string.digits) for num in range(19))
#     #     verifyFp = "verify_YOUR_VERIFYFP_HERE"
#     #     api = TikTokApi.get_instance(
#     #         use_selenium=True, custom_verifyFp=verifyFp, custom_did=did)
#     #     # print(api.byUsername(name))
#     #     count = 1
#     #     tiktoks = api.byHashtag(name, count, language='en', proxy=None)
#     #     Path("downloads").mkdir(exist_ok=True)
#     #     n = 1
#     #     for i in range(n):
#     #         r = 1
#     #         data = api.get_Video_By_TikTok(tiktoks[r])  # bytes of the video
#     #         with open("downloads/video.mp4".format(str(r)), 'wb') as output:
#     #             output.write(data)
#     #     await ctx.send(file=discord.File(r'downloads/video.mp4'))


def setup(bot):
    bot.add_cog(TikTok(bot))
