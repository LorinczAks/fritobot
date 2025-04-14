# fritobot
This discord bot is able to join your voice channel and play the desired songs from youtube either using search queries or youtube urls.
It can hold a queue of songs as well. Basic functions like skipping and pausing are implemented.
Here is the full list of features:

*Welcome to fritobot help page! If you have further questions, feel free to reach out at @realaki on discord  
/play [yt url]/[search query]/[playlist] - plays searched song(s); if the bot is playing, adds it to queue  
/queue - shows songs currently in queue  
/pause - pauses playback  
/resume - resumes playback  
/skip - skips current song  
/remove - removes the latest added song from queue  
/clearq - removes all songs from queue  
/stop - stops playback, deletes queue and leaves voice channel  
/help - shows this manual*

### Creating your own bot
You can read about how to create and get started with your own bot in [discord developer documentation](https://discord.com/developers/docs/intro)

### Token
In order for your code to be able to use environment variables like your discord bot token, you need to create an .env file in main.py's directory and have
```
BOT_TOKEN=your-bot-token-goes-here
```
in it.  
For a detailed explanation on using environmental variables in python, I recommend [this page](https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5).