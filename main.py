from youtube_dl import YoutubeDL
from functools import partial
from async_timeout import timeout
import traceback
import sys
import itertools
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


@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')
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

    if "rr" in message.content:
        await message.channel.send('https://discord.gg/rcRzaQKWKX')


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

# youtube_dl.utils.bug_reports_message = lambda: ''


# ytdl_format_options = {
#     'format': 'bestaudio/best',
#     'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
#     'restrictfilenames': True,
#     'noplaylist': True,
#     'nocheckcertificate': True,
#     'ignoreerrors': False,
#     'logtostderr': False,
#     'quiet': True,
#     'no_warnings': True,
#     'default_search': 'auto',
#     # bind to ipv4 since ipv6 addresses cause issues sometimes
#     'source_address': '0.0.0.0'
# }

# ffmpeg_options = {
#     'options': '-vn'
# }

# ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


# queues = {}


# class YTDLSource(discord.PCMVolumeTransformer):
#     def __init__(self, source, *, data, volume=0.5):
#         super().__init__(source, volume)

#         self.data = data

#         self.title = data.get('title')
#         self.url = data.get('url')

#     @classmethod
#     async def from_url(cls, url, *, loop=None, stream=False):
#         loop = loop or asyncio.get_event_loop()
#         data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

#         if 'entries' in data:
#             # take first item from a playlist
#             data = data['entries'][0]

#         filename = data['url'] if stream else ytdl.prepare_filename(data)
#         return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


# class Music(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot

#     @commands.command()
#     async def join(self, ctx, *, channel: discord.VoiceChannel):
#         """Joins a voice channel"""

#         if ctx.voice_client is not None:
#             return await ctx.voice_client.move_to(channel)

#         await channel.connect()

#     @commands.command()
#     async def playlocal(self, ctx, *, query):
#         """Plays a file from the local filesystem"""

#         source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
#         ctx.voice_client.play(source, after=lambda e: print(
#             'Player error: %s' % e) if e else None)

#         await ctx.send('Now playing: {}'.format(query))

#     @commands.command()
#     async def ytdownplay(self, ctx, *, url):
#         """Plays from a url (almost anything youtube_dl supports)"""

#         async with ctx.typing():
#             player = await YTDLSource.from_url(url, loop=self.bot.loop)
#             ctx.voice_client.play(player, after=lambda e: print(
#                 'Player error: %s' % e) if e else None)

#         await ctx.send('Now playing: {}'.format(player.title))

#     # @commands.command()
#     # async def play(self, ctx, *, url):
#     #     """Streams from a url (same as yt, but doesn't predownload)"""

#     #     async with ctx.typing():
#     #         player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
#     #         ctx.voice_client.play(player, after=lambda e: print(
#     #             'Player error: %s' % e) if e else None)

#     #     await ctx.send('Now playing: {}'.format(player.title))

#     @commands.command()
#     async def play(self, ctx, *, url):
#         """Streams from a url (same as yt, but doesn't predownload)"""

#         async with ctx.typing():

#             if ctx.voice_client.is_playing():
#                 await self.q(ctx, url)
#                 #ctx.send('Queued...')

#             else:
#                 player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
#                 ctx.voice_client.play(player, after=lambda e: print(
#                     'Player error: %s' % e) if e else None)

#                 await ctx.send('Now playing: {}'.format(player.title))


#     async def q(self, ctx, url):
#         #server = ctx.message.server

#         player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
#         ctx.voice_client.play(player, after=lambda e: print(
#             'Player error: %s' % e) if e else None)

#         queues.append(player)

#         await self.bot.say("queued")


#     @commands.command()
#     async def volume(self, ctx, volume: int):
#         """Changes the player's volume"""

#         if ctx.voice_client is None:
#             return await ctx.send("Not connected to a voice channel.")

#         ctx.voice_client.source.volume = volume / 100
#         await ctx.send("Changed volume to {}%".format(volume))

#     @commands.command()
#     async def pause(self, ctx):
#         if ctx.voice_client.is_playing():
#             ctx.voice_client.pause()
#         else:
#             await ctx.send("Currently no audio is playing.")

#     @commands.command()
#     async def resume(self, ctx):
#         if ctx.voice_client.is_paused():
#             ctx.voice_client.resume()
#         else:
#             await ctx.send("The audio is not paused.")

#     @commands.command()
#     async def stop(self, ctx):
#         """Stops and disconnects the bot from voice"""

#         await ctx.voice_client.disconnect()

#     @playlocal.before_invoke
#     @ytdownplay.before_invoke
#     @play.before_invoke
#     async def ensure_voice(self, ctx):
#         if ctx.voice_client is None:
#             if ctx.author.voice:
#                 await ctx.author.voice.channel.connect()
#             else:
#                 await ctx.send("You are not connected to a voice channel.")
#                 raise commands.CommandError(
#                     "Author not connected to a voice channel.")
#         elif ctx.voice_client.is_playing():
#             ctx.voice_client.stop()


# bot.add_cog(Music(bot))


#############################################
ytdlopts = {
    'format': 'bestaudio/best',
    'default_search': 'auto',
    # 'restrictfilenames': True,
    # 'noplaylist': True,
    # 'nocheckcertificate': True,
    # 'ignoreerrors': False,
    # 'logtostderr': False,
    # 'quiet': True,
    # 'no_warnings': True,
    # 'default_search': 'auto',
    # 'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        await ctx.send(f'```ini\n[Added {data["title"]} to the Queue.]\n```', delete_after=15)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info,
                         url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer:
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice it's instance will be destroyed.
    """

    __slots__ = ('bot', '_guild', '_channel', '_cog',
                 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                if self in self._cog.players.values():
                    return self.destroy(self._guild)
                return

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'There was an error processing your song.\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(
                source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(f'**Now Playing:** `{source.title}` requested by '
                                               f'`{source.requester}`')
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

            try:
                # We are no longer playing this song...
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):
    """Music related commands."""

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            for entry in self.players[guild.id].queue._queue:
                if isinstance(entry, YTDLSource):
                    entry.cleanup()
            self.players[guild.id].queue._queue.clear()
        except KeyError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('This command can not be used in Private Messages.')
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send('Error connecting to Voice Channel. '
                           'Please make sure you are in a valid channel or provide me with one')

        print('Ignoring exception in command {}:'.format(
            ctx.command), file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.command(name='connect', aliases=['join'])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):
        """Connect to voice.
        Parameters
        ------------
        channel: discord.VoiceChannel [Optional]
            The channel to connect to. If a channel is not specified, an attempt to join the voice channel you are in
            will be made.
        This command also handles moving the bot to different channels.
        """
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise InvalidVoiceChannel(
                    'No channel to join. Please either specify a valid channel or join one.')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(
                    f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(
                    f'Connecting to channel: <{channel}> timed out.')

        await ctx.send(f'Connected to: **{channel}**', delete_after=20)

    @commands.command(name='play', aliases=['sing'])
    async def play_(self, ctx, *, search: str):
        """Request a song and add it to the queue.
        This command attempts to join a valid voice channel if the bot is not already in one.
        Uses YTDL to automatically search and retrieve a song.
        Parameters
        ------------
        search: str [Required]
            The song to search and retrieve using YTDL. This could be a simple search, an ID or URL.
        """
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        # If download is False, source will be a dict which will be used later to regather the stream.
        # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await player.queue.put(source)

    @commands.command(name='loop', aliases=['singloop'])
    async def loop_(self, ctx, times: int, *, search: str):
        """Request a song and add it to the queue.
        This command attempts to join a valid voice channel if the bot is not already in one.
        Uses YTDL to automatically search and retrieve a song.
        Parameters
        ------------
        search: str [Required]
            The song to search and retrieve using YTDL. This could be a simple search, an ID or URL.
        """
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        # If download is False, source will be a dict which will be used later to regather the stream.
        # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)
        await player.queue.put(source)

        for i in range(times):
            await player.queue.put(source)

    @commands.command(name='pause')
    async def pause_(self, ctx):
        """Pause the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send('I am not currently playing anything!', delete_after=20)
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.send(f'**`{ctx.author}`**: Paused the song!')

    @commands.command(name='resume')
    async def resume_(self, ctx):
        """Resume the currently paused song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=20)
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.send(f'**`{ctx.author}`**: Resumed the song!')

    @commands.command(name='skip')
    async def skip_(self, ctx):
        """Skip the song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=20)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
        await ctx.send(f'**`{ctx.author}`**: Skipped the song!')

    @commands.command(name='queue', aliases=['q', 'playlist'])
    async def queue_info(self, ctx):
        """Retrieve a basic queue of upcoming songs."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', delete_after=20)

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send('There are currently no more queued songs.')

        # Grab up to 5 entries from the queue...
        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        fmt = '\n'.join(f'**`{_["title"]}`**' for _ in upcoming)
        embed = discord.Embed(
            title=f'Upcoming - Next {len(upcoming)}', description=fmt)

        await ctx.send(embed=embed)

    @commands.command(name='now_playing', aliases=['np', 'current', 'currentsong', 'playing'])
    async def now_playing_(self, ctx):
        """Display information about the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', delete_after=20)

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send('I am not currently playing anything!')

        try:
            # Remove our previous now_playing message.
            await player.np.delete()
        except discord.HTTPException:
            pass

        player.np = await ctx.send(f'**Now Playing:** `{vc.source.title}` '
                                   f'requested by `{vc.source.requester}`')

    @commands.command(name='volume', aliases=['vol'])
    async def change_volume(self, ctx, *, vol: float):
        """Change the player volume.
        Parameters
        ------------
        volume: float or int [Required]
            The volume to set the player to in percentage. This must be between 1 and 100.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', delete_after=20)

        if not 0 < vol < 101:
            return await ctx.send('Please enter a value between 1 and 100.')

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        await ctx.send(f'**`{ctx.author}`**: Set the volume to **{vol}%**')

    @commands.command(name='stop')
    async def stop_(self, ctx):
        """Stop the currently playing song and destroy the player.
        !Warning!
            This will destroy the player assigned to your guild, also deleting any queued songs and settings.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=20)

        await self.cleanup(ctx.guild)


# def setup(bot):

bot.add_cog(Music(bot))


bot.run(os.getenv('TOKEN'))
