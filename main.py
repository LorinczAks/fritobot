import asyncio
from decouple import config
import discord
import random


import fritobot

intents = discord.Intents.default()
intents.message_content = True

client = fritobot.fritobot(intents=intents)

BOT_TOKEN = config('BOT_TOKEN')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    query = message.content.split(" ")
    if query[0] == '/play':
        if 'list=' in query[1]:
            songs = await client.search_playlist(query[1])
            if not songs:
                await message.channel.send("```Couldn't find any results for that query```")
                return
            while(songs):
                song = songs.pop(0)
                if not client.is_playing:
                    if message.author.voice is None:
                        await message.channel.send("```Join a voice channel to use bot!```")
                        return
                    channel_to_join = message.author.voice.channel
                    if client.vc is None:
                        client.vc = await channel_to_join.connect()

                    client.music_queue.append((song['source'], song['title'], song['url']))
                    await message.channel.send(f"```Playing {song['title']}```")
                    await client.play_next()
                else:
                    client.music_queue.append((song['source'], song['title'], song['url']))
                    await message.channel.send(f"```Added {song['title']} to queue```")
        else:
            song = await client.search_yt(' '.join(query[1:]))
            if not song:
                await message.channel.send("```Couldn't find any results for that query```")
                return

            if not client.is_playing:
                # If nothing is playing, start playback immediately
                if message.author.voice is None:
                    await message.channel.send("```Join a voice channel to use bot!```")
                    return
                channel_to_join = message.author.voice.channel
                if client.vc is None:
                    client.vc = await channel_to_join.connect()

                client.music_queue.append((song['source'], song['title'], song['url']))
                await message.channel.send(f"```Playing {song['title']}```")
                await client.play_next()
            else:
                # If something is playing, just add the song to the queue
                client.music_queue.append((song['source'], song['title'], song['url']))
                await message.channel.send(f"```Added {song['title']} to queue```")    
    elif query[0] == '/next':
        # puts song next in queue
        song = await client.search_yt(' '.join(query[1:]))
        if not song:
            await message.channel.send("```Couldn't find any results for that query```")
            return

        if not client.is_playing:
            # If nothing is playing, start playback immediately
            if message.author.voice is None:
                await message.channel.send("```Join a voice channel to use bot!```")
                return
            channel_to_join = message.author.voice.channel
            if client.vc is None:
                client.vc = await channel_to_join.connect()

            client.music_queue.append((song['source'], song['title'], song['url']))
            await message.channel.send(f"```Playing {song['title']}```")
            await client.play_next()
        else:
            client.music_queue.insert(0, (song['source'], song['title'], song['url']))
            await message.channel.send(f"```Added {song['title']} to play next```")
    elif query[0] == '/queue':
        # showing songs currently in queue
        if len(client.music_queue) == 0:
            await message.channel.send("```There are currently no songs in queue```")
        else:
            await message.channel.send(f"```{len(client.music_queue)} songs in queue. Next 10 songs in queue:\n{'\n'.join([f'{item[1]}' for item in client.music_queue[:10]])}```")
    elif query[0] == '/shuffle':
        # shuffles queue
        if len(client.music_queue) == 0:
            await message.channel.send("```There are currently no songs in queue```")
        else:
            random.shuffle(client.music_queue)
            await message.channel.send(f"```Queue shuffled```")
    elif query[0] == '/stop':
        # stopping playback, deleting queue and leaving voice channel
        client.music_queue.clear()
        client.vc.stop()
        await asyncio.sleep(1)
        await client.vc.disconnect()
        client.vc = None
        await message.channel.send("```Deleted queue and left voice channel. Goodbye! <3```")
        client.is_playing = False
    elif query[0] == '/skip':
        # stopping playback. since playing music is happening in loop, the next song starts playing
        client.vc.stop()
        await message.channel.send("```Skipped current song```")
        await asyncio.sleep(1)
        await client.play_next()
    elif query[0] == '/pause':
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
    elif query[0] == '/resume':
        # resuming playback
        if client.is_paused:
            await message.channel.send("```Resumed playback```")
            client.is_paused = False
            client.is_playing = True
            client.vc.resume()
    elif query[0] == '/remove':
        # removing last song from queue
        if len(client.music_queue) > 0:
            client.music_queue.pop()
            await message.channel.send("```Last song removed from queue```")
        else:
            await message.channel.send("```Queue is empty!```")
    elif query[0] == '/clearq':
        # removing all songs from queue
        if len(client.music_queue) > 0:
            client.music_queue = []
            await message.channel.send("```Queue cleared```")
        else:
            await message.channel.send("```Queue is already empty!```")
    elif query[0] == '/help':
        # sending information about commands
        await message.channel.send(
            f"""
```
Welcome to fritobot help page! If you have further questions, feel free to reach out at @realaki on discord
/play [yt url]/[search query]/[playlist] - plays searched song(s); if the bot is playing, adds it to queue
/next [yt url]/[search query] - adds song to queue to play next
/queue - shows info about song queue
/shuffle - shuffles song queue
/pause - pauses playback
/resume - resumes playback
/skip - skips current song
/remove - removes the latest added song from queue
/clearq - removes all songs from queue
/stop - stops playback, deletes queue and leaves voice channel
/help - shows this manual
```
            """
            )

client.run(BOT_TOKEN)
