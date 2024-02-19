import fritobot
import discord
from decouple import config
import asyncio

intents = discord.Intents.default()
intents.message_content = True

client = fritobot.fritobot(intents=intents)

# grabbing bot token from env file
BOT_TOKEN = config('BOT_TOKEN')

FFMPEG_OPTIONS = {'options': '-vn',
                  "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                  }

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/play'):
        # implementing playing a song if nothing is playing currently
        if not client.is_playing:
            query = ' '.join(message.content.split(" ")[1:])
            # to join voice channel and start playing the song
            if message.author.voice == None:
                await message.channel.send("```Join a voice channel to use bot!```")
                return
            channel_to_join = message.author.voice.channel
            if client.vc == None:
                client.vc = await channel_to_join.connect()
            
            song = client.search_yt(query)
            data = client.ytdl.extract_info(song['source'], download=False)
            client.music_queue.append((data['url'], data['title']))
            await message.channel.send(f"```Playing {data['title']}```")
            await client.play_next()
        else:
            # its already playing so we append the song to the queue
            query = ' '.join(message.content.split(" ")[1:])
            song = client.search_yt(query)
            data = client.ytdl.extract_info(song['source'], download=False)
            await message.channel.send(f"```Added {data['title']} to queue```")
            client.music_queue.append((data['url'], data['title']))
    elif message.content.startswith('/queue'):
        # showing songs currently in queue
        if len(client.music_queue) == 0:
            await message.channel.send("```There are currently no songs in queue```")
        else:
            await message.channel.send(f"```Song queue:\n{'\n'.join([f'{item[1]}' for item in client.music_queue])}```")
    elif message.content.startswith('/stop'):
        # stopping playback, deleting queue and leaving voice channel
        client.music_queue.clear()
        client.vc.stop()
        await asyncio.sleep(1)
        await client.vc.disconnect()
        client.vc = None
        await message.channel.send("```Deleted queue and left voice channel. Goodbye! <3```")
        client.is_playing = False
    elif message.content.startswith('/skip'):
        # stopping playback. since playing music is happening in loop, the next song starts playing
        client.vc.stop()
        await message.channel.send("```Skipped current song```")
        await asyncio.sleep(1)
        await client.play_next()
    elif message.content.startswith('/pause'):
        # implementing pausing/resuming playback
        if client.is_playing:
            await message.channel.send("```Paused playback```")
            client.is_playing = False
            client.is_paused = True
            client.vc.pause()
        elif client.is_paused:
            await message.channel.send("```Resumed playback```")
            client.is_paused = False
            client.is_playing = True
            client.vc.resume()
    elif message.content.startswith('/resume'):
        # resuming playback
        if client.is_paused:
            await message.channel.send("```Resumed playback```")
            client.is_paused = False
            client.is_playing = True
            client.vc.resume()
    elif message.content.startswith('/remove'):
        # removing last song from queue
        if len(client.music_queue) > 0:
            client.music_queue.pop()
            await message.channel.send("```Last song removed from queue```")
        else:
            await message.channel.send("```Queue is empty! Maybe you want to use /stop```")
    elif message.content.startswith('/help'):
        # sending information about commands
        await message.channel.send(
            f"""
```
Welcome to fritobot help page! If you have further questions, feel free to reach out at @realaki on discord
/play [yt url]/[search query] - plays searched song; if the bot is playing, adds it to queue
/queue - shows songs currently in queue
/pause - pauses playback
/resume - resumes playback
/skip - skips current song
/remove - removes the latest added song from queue
/stop - stops playback, deletes queue and leaves voice channel
/help - shows this manual
```
            """
            )

client.run(BOT_TOKEN)
