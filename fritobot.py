from decouple import config
import discord
from yt_dlp import YoutubeDL
import youtubesearchpython
import asyncio

FFMPEG_OPTIONS = {'options': '-vn',
                  "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                  }


class fritobot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vc = None
        self.music_queue = []
        self.ytdl = YoutubeDL({'format': 'bestaudio/best'})

        self.vc = None
        self.is_playing = False
        self.is_paused = False


    # methods
    def search_yt(self, item):
        if item.startswith("https://"):
            title = self.ytdl.extract_info(item, download=False)["title"]
            return{'source':item, 'title':title}
        
        search = youtubesearchpython.VideosSearch(item, limit=1)
        return{'source':search.result()["result"][0]["link"], 'title':search.result()["result"][0]["title"]}


    async def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            tmp_url = self.music_queue[0][0]

            self.music_queue.pop(0)
            loop = asyncio.get_event_loop()
            data = self.ytdl.extract_info(tmp_url, download=False)
            self.vc.play(discord.FFmpegPCMAudio(data['url'], executable= "ffmpeg.exe", **FFMPEG_OPTIONS),
                         after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), loop))
        else:
            self.is_playing = False

