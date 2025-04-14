import asyncio
import discord
import functools
from yt_dlp import YoutubeDL

FFMPEG_OPTIONS = {'options': '-vn -sn -dn',
                  "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                  }


class fritobot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vc = None
        self.music_queue = []
        self.ytdl = YoutubeDL({'format': 'bestaudio/best', 'ignoreerrors': True, 'ignore_no_formats_error': True, 'quiet': True}) 
        self.is_playing = False
        self.is_paused = False

    async def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            data = self.music_queue.pop(0)

            loop = asyncio.get_running_loop()
            self.vc.play(discord.FFmpegOpusAudio(data[2], executable="ffmpeg.exe", **FFMPEG_OPTIONS),
                        after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), loop))
        else:
            self.is_playing = False

    async def search_yt(self, item):
        loop = asyncio.get_running_loop()
        if item.startswith("https://"):
            info = await loop.run_in_executor(None, functools.partial(self.ytdl.extract_info, item, False))
            return {'source': item, 'title': info['title'], 'url': info['url']}

        item = f"ytsearch:{item}"
        info = await loop.run_in_executor(None, functools.partial(self.ytdl.extract_info, item, False))

        if not info or 'entries' not in info or len(info['entries']) == 0:
            return None

        entry = info['entries'][0]
        return {'source': entry['webpage_url'], 'title': entry['title'], 'url': entry['url']}

    async def search_playlist(self, item):
        result = []
        loop = asyncio.get_running_loop()
        info = await loop.run_in_executor(None, functools.partial(self.ytdl.extract_info, item, False))
        for elem in info['entries']:
            if 'webpage_url' in elem and 'title' in elem and 'url' in elem:
                result.append({'source': elem['webpage_url'], 'title': elem['title'], 'url': elem['url']})
        return result