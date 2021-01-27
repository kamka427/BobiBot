import discord
import os

client = discord.Client()


@client.event
async def on_ready():
    print('{0.user} has connected to Discord!'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Yo!')




client.run(os.getenv('TOKEN'))
