# This example requires the 'message_content' intent.

import fritobot
import discord
from decouple import config

intents = discord.Intents.default()
intents.message_content = True

client = fritobot.fritobot(intents=intents)
BOT_TOKEN = config('BOT_TOKEN')

FFMPEG_OPTIONS = {'options': '-vn'}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/play'):
        if not client.is_playing:
            url = message.content.split(" ")[1]
            # to join voice channel and start playing the song
            channel_to_join = message.author.voice.channel
            client.vc = await channel_to_join.connect()

            data = client.ytdl.extract_info(url, download=False)
            song = data['url']
            client.vc.play(discord.FFmpegPCMAudio(song, executable= "ffmpeg.exe", **FFMPEG_OPTIONS))
            client.is_playing = True
        else:
            # its already playing so we append the song to the queue
            url = message.content.split(" ")[1]
            await message.channel.send(f'Added {client.search_yt(url)['title']} to queue')
            client.music_queue.append(client.search_yt(url)['source'])




client.run(BOT_TOKEN)
