import os
from discord.ext import commands
import discord
from pathlib import Path
from random import randint
from pprint import pprint
from TikTokAPI import TikTokAPI
import nest_asyncio

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
        try:
            nest_asyncio.apply()
            user = api.getVideosByUserName(name, count=10)
            video = user['items'][randint(0, 9)]['video']['id']
            api.downloadVideoById(
                video, './downloads/{}.mp4'.format((str("v"))))
            await ctx.send(file=discord.File('./downloads/v.mp4'))
        except:
            print("Volt egy hiba...")

    @commands.command(aliases=['Tok'])
    async def tok(self, ctx, name):
        try:
            nest_asyncio.apply()
            user = api.getVideosByHashTag(name, count=10)
            video = user['itemList'][randint(0, 9)]['video']['id']
            api.downloadVideoById(
                video, './downloads/{}.mp4'.format((str("v"))))
            await ctx.send(file=discord.File('./downloads/v.mp4'))
        except:
            print("Volt egy hiba...")


def setup(bot):
    bot.add_cog(TikTok(bot))
