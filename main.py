from dotenv import load_dotenv
import discord
import os

client = discord.Client()


load_dotenv()


@client.event
async def on_ready():
    print('{0.user} has connected to Discord!'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('Yo!')

    if message.content.startswith('yo'):
        await message.channel.send('yo yo yo!')

# token = os.getenv('TOKEN')
client.run(os.getenv('TOKEN'))
