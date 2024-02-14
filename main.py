# This example requires the 'message_content' intent.

import os
from decouple import config
import discord
from yt_dlp import YoutubeDL
#from youtubesearchpython import VideosSearch

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
BOT_TOKEN = config('BOT_TOKEN')

# setting up variables

music_queue = []
ytdl = YoutubeDL({'format': 'bestaudio/best'})

vc = None
is_playing = False
is_paused = False



# methods
def search_yt(item):
    if item.startswith("https://"):
        title = ytdl.extract_info(item, download=False)["title"]
        print(title)
        return{'source':item, 'title':title}
    
    #search = VideosSearch(item, limit=1)
    #return{'source':search.result()["result"][0]["link"], 'title':search.result()["result"][0]["title"]}


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/play'):
        url = message.content.split(" ")[1]
        #print(f'{message.content}, {url}')
        await message.channel.send(f'Added {search_yt(url)['title']} to queue')

client.run(BOT_TOKEN)
