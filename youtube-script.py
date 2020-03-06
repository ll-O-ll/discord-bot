# @client.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl'])
# async def play(ctx, url: str):

song_there = os.path.isfile("song.mp3")
try:
    if song_there:
        os.remove("song.mp3")
except PermissionError:
    await ctx.send("Wait for the current playing music end or use the 'stop' command")
    return
await ctx.send("Getting everything ready, playing audio soon")
print("Someone wants to play music let me get that ready for them...")
voice = get(bot.voice_clients, guild=ctx.guild)
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
for file in os.listdir("./"):
    if file.endswith(".mp3"):
        os.rename(file, 'song.mp3')
voice.play(discord.FFmpegPCMAudio("song.mp3"))
voice.volume = 100
voice.is_playing()