from decouple import config
import discord
from yt_dlp import YoutubeDL




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
        print(title)
        return{'source':item, 'title':title}
    
    #search = VideosSearch(item, limit=1)
    #return{'source':search.result()["result"][0]["link"], 'title':search.result()["result"][0]["title"]}


