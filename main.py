import ctypes
import ctypes.util
import math
import functools
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import praw
import random
import youtube_dl
import asyncio
from async_timeout import timeout
import itertools


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

    if message.content == 'v':
        await message.channel.send('guys v?')

    if message.content.startswith('rahim'):
        await message.channel.send('https://cdn.discordapp.com/attachments/546393279827017729/804093858005647400/Cd7DPJqWEAEcRm9.jpg')

    if message.content == 'rr':
        await message.channel.send('https://discord.gg/rcRzaQKWKX')

    if "gacha" in message.content:
        await message.channel.send('game king')

    if message.content == 'lolpatch':
        await message.channel.send('https://na.leagueoflegends.com/en-us/news/tags/patch-notes')


@bot.command()
async def m(ctx, *, user: discord.Member = None):
    if user:
        await ctx.send(f"{user.mention}, get yo A$$ here!")
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


@bot.command(aliases=['Waifu'])
async def waifu(ctx):
    submission = reddit.subreddit("Waifu").random()
    m = await ctx.send(submission.url)
    await m.add_reaction("❤")
    await ctx.send("She is a " + str(random.randint(1, 5)) + " star waifu!")


@bot.command(aliases=['Trap'])
async def trap(ctx):
    submission = reddit.subreddit("astolfo").random()
    await ctx.send(submission.url)


@bot.command(aliases=['Peepo'])
async def peepo(ctx):
    submission = reddit.subreddit("peepos").random()
    await ctx.send(submission.url)


@bot.command(aliases=['Movie'])
async def movie(ctx):
    submission = reddit.subreddit("trailers").random()
    await ctx.send(submission.url)


@bot.command(aliases=['Reddit'])
async def r(ctx, name):
    submission = reddit.subreddit(name).random()
    await ctx.send(submission.url)


@bot.command(aliases=['Husbando'])
async def husbando(ctx, name):
    await ctx.send(name + " ,you are a " + str(random.randint(1, 5)) + " star husbando!")


@bot.command(aliases=['Waifure'])
async def waifure(ctx, name):
    await ctx.send(name + " is a " + str(random.randint(1, 5)) + " star waifu!")

########################################################################################################################################################################
# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ''


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': False,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(
            cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError(
                'Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError(
                    'Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(
            cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError(
                        'Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='Now playing',
                               description='```css\n{0.source.title}\n```'.format(
                                   self),
                               color=discord.Color.blurple())
                 .add_field(name='Duration', value=self.source.duration)
                 .add_field(name='Requested by', value=self.requester.mention)
                 .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='URL', value='[Click]({0.source.url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))

        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.now = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()
        self.exists = True

        self._loop = False
        self._volume = 1
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                # Try to get the next song within 3 minutes.
                # If no song will be added to the queue in time,
                # the player will disconnect due to performance
                # reasons.
                try:
                    async with timeout(180):  # 3 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    self.exists = False
                    return

                self.current.source.volume = self._volume
                self.voice.play(self.current.source, after=self.play_next_song)
                await self.current.source.channel.send(embed=self.current.create_embed())

            elif self.loop:

                self.now = discord.FFmpegPCMAudio(
                    self.current.source.stream_url, **YTDLSource.FFMPEG_OPTIONS)
                #self.now.source.volume = self._volume
                self.voice.play(self.now,
                                after=self.play_next_song)

            await self.next.wait()

            # If the song is looped

            #     self.voice.play(self.current.source,
            #                     after=self.play_next_song)

            # await self.next.wait()

    def play_next_song(self, error=None):

        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state or not state.exists:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage(
                'This command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('An error occurred: {}'.format(str(error)))

    @commands.command(name='join', invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        """Joins a voice channel."""

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='summon')
    @commands.has_permissions(manage_guild=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        """Summons the bot to a voice channel.
        If no channel was specified, it joins your channel.
        """

        if not channel and not ctx.author.voice:
            raise VoiceError(
                'You are neither connected to a voice channel nor specified a channel to join.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='leave', aliases=['disconnect'])
    @commands.has_permissions(manage_guild=True)
    async def _leave(self, ctx: commands.Context):
        """Clears the queue and leaves the voice channel."""

        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command(name='volume')
    async def _volume(self, ctx: commands.Context, *, volume: int):
        """Sets the volume of the player."""

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        if 0 > volume > 100:
            return await ctx.send('Volume must be between 0 and 100')

        ctx.voice_client.source.volume = volume / 100
        #ctx.voice_client.volume = volume / 100
        #ctx.voice_client.now.volume = volume / 100
        # ctx.voice_state.volume = volume / 100
        #ctx.now.volume = volume / 100
        # ctx.voice_state.volume = volume / 100
        await ctx.send('Volume of the player set to {}%'.format(volume))

    @commands.command(name='now', aliases=['current', 'playing'])
    async def _now(self, ctx: commands.Context):
        """Displays the currently playing song."""

        await ctx.send(embed=ctx.voice_state.current.create_embed())

    # @commands.command()
    # async def pause(self, ctx):
    #     if ctx.voice_client.is_playing():
    #         ctx.voice_client.pause()
    #     else:
    #         await ctx.send("Currently no audio is playing.")

    # @commands.command()
    # async def resume(self, ctx):
    #     if ctx.voice_client.is_paused():
    #         ctx.voice_client.resume()
    #     else:
    #         await ctx.send("The audio is not paused.")

    @commands.command(name='pause')
    # @commands.has_permissions(manage_guild=True)
    async def _pause(self, ctx: commands.Context):
        """Pauses the currently playing song."""

        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.message.add_reaction('⏯')
        else:
            await ctx.send("Currently no audio is playing.")

    @commands.command(name='resume')
    # @commands.has_permissions(manage_guild=True)
    async def _resume(self, ctx: commands.Context):
        """Resumes a currently paused song."""
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.message.add_reaction('⏯')
        else:
            await ctx.send("The audio is not paused.")

    # @commands.command(name='pause')
    # @commands.has_permissions(manage_guild=True)
    # async def _pause(self, ctx: commands.Context):
    #     """Pauses the currently playing song."""

    #     if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
    #         ctx.voice_state.voice.pause()
    #         await ctx.message.add_reaction('⏯')

    # @commands.command(name='resume')
    # @commands.has_permissions(manage_guild=True)
    # async def _resume(self, ctx: commands.Context):
    #     """Resumes a currently paused song."""

    #     if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
    #         ctx.voice_state.voice.resume()
    #         await ctx.message.add_reaction('⏯')

    # @commands.command()
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

    @commands.command(name='stop')
    @commands.has_permissions(manage_guild=True)
    async def _stop(self, ctx: commands.Context):
        """Stops playing song and clears the queue."""

        ctx.voice_state.songs.clear()

        if not ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')

    @commands.command(name='skip')
    async def _skip(self, ctx: commands.Context):
        """Vote to skip a song. The requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Not playing any music right now...')

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
            else:
                await ctx.send('Skip vote added, currently at **{}/3**'.format(total_votes))

        else:
            await ctx.send('You have already voted to skip this song.')

    @commands.command(name='queue')
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        """Shows the player's queue.
        You can optionally specify the page to show. Each page contains 10 elements.
        """

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(
                i + 1, song)

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @commands.command(name='shuffle')
    async def _shuffle(self, ctx: commands.Context):
        """Shuffles the queue."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(name='remove')
    async def _remove(self, ctx: commands.Context, index: int):
        """Removes a song from the queue at a given index."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @commands.command()
    async def stop1(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @commands.command(name='loop')
    async def _loop(self, ctx: commands.Context):
        """Loops the currently playing song.
        Invoke this command again to unloop the song.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')

    @commands.command(name='play')
    async def _play(self, ctx: commands.Context, *, search: str):
        """Plays a song.
        If there are songs in the queue, this will be queued until the
        other songs finished playing.
        This command automatically searches from various sites if no URL is provided.
        A list of these sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
        """

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await ctx.send('Enqueued {}'.format(str(source)))

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError(
                'You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError(
                    'Bot is already in a voice channel.')

    @commands.command(name='search')
    async def _search(self, ctx: commands.Context, *, search: str):
        """Searches youtube.
        It returns an imbed of the first 10 results collected from youtube.
        Then the user can choose one of the titles by typing a number
        in chat or they can cancel by typing "cancel" in chat.
        Each title in the list can be clicked as a link.
        """
        async with ctx.typing():
            try:
                source = await YTDLSource.search_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
            else:
                if source == 'sel_invalid':
                    await ctx.send('Invalid selection')
                elif source == 'cancel':
                    await ctx.send(':white_check_mark:')
                elif source == 'timeout':
                    await ctx.send(':alarm_clock: **Time\'s up bud**')
                else:
                    if not ctx.voice_state.voice:
                        await ctx.invoke(self._join)

                    song = Song(source)
                    await ctx.voice_state.songs.put(song)
                    await ctx.send('Enqueued {}'.format(str(source)))

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError(
                'You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError(
                    'Bot is already in a voice channel.')


bot.add_cog(Music(bot))


@bot.command(name='botstop', aliases=['bstop'])
@commands.is_owner()
async def botstop(ctx):
    print('Goodbye')
    await ctx.send('Goodbye')
    await bot.logout()
    return

bot.run(os.getenv('TOKEN'))
