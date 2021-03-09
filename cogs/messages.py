from discord.ext import commands
import discord
import random

class Messages(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message, user: discord.Member = None):
        if (message.author.bot):
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

        if message.content == 'v':
            await message.channel.send('guys v?')

        if message.content.startswith('rahim'):
            await message.channel.send('https://cdn.discordapp.com/attachments/546393279827017729/804093858005647400/Cd7DPJqWEAEcRm9.jpg')

        if message.content == 'rr':
            await message.channel.send('https://discord.gg/rcRzaQKWKX')

        if "gacha" in message.content:
            await message.channel.send('game king')

        if message.content == 'lolpatch':
            await message.channel.send('https://na.leagueoflegends.com/en-us/news/tags/ patch-notes')

        # if message.content.startswith('-p'):
        #     await message.channel.send('https://media.tenor.com/images/254629658d75071285e84502d71c67c1/tenor.gif')

    @commands.command()
    async def m(self, ctx, *, user: discord.Member = None):
        if user:
            await ctx.send(f"{user.mention}, get yo A$$ here!")
        else:
            await ctx.send('You have to say who needs to get his/her a$$    here!')

    @commands.command()
    async def repeat(self, ctx, times: int, content='Repeating...'):
        """Tobbszor megismetel egy uzenetet."""
        for i in range(times):
            await ctx.send(content)

    @commands.command(description='Nem tudsz valamit eldonteni?')
    async def choose(self, ctx, *choices: str):
        """Egyet valaszt a lehetosegekbol."""
        await ctx.send(random.choice(choices))

    @commands.command()
    async def roll(self, ctx, dice: str):
        """Rolls a dice in N*N format."""
        try:
            rolls, limit = map(int, dice.split('*'))
        except Exception:
            await ctx.send('Format has to be in N*N!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command(aliases=['Husbando'])
    async def husbando(self, ctx, name):
        await ctx.send(name + ", you are a " + str(random.randint(1, 5)) + " star husbando!")

    @commands.command(aliases=['Waifure'])
    async def waifure(self, ctx, name):
        await ctx.send(name + " is a " + str(random.randint(1, 5)) + " star waifu!")


def setup(bot):
    bot.add_cog(Messages(bot))
