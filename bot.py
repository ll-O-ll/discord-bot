import discord
import asyncio
import youtube_dl
from os import system
from itertools import cycle
from discord.utils import get
from discord.ext import commands
from discord import FFmpegPCMAudio

# /********************INCLUDE TOKEN BEFORE TEST********************************/

TOKEN = ''

client = commands.Bot(command_prefix = '.')
client.remove_command('help')
states = ["bored face ... \U0001f61e", "with the API... \U0001f603", " with user requests... \U0001f916"]
player = {}
queues = {}

async def change_status():
    await client.wait_until_ready()
    msgs = cycle(states)
    while not client.is_closed():
        current_status = next(msgs)
        game = discord.Game(name=current_status)
        await client.change_presence(activity=game) 
        await asyncio.sleep(5)

@client.event
async def on_ready():
    game = discord.Game(name="with the API... \U0001f603")
    await client.change_presence(activity=game)  
    print('Bot {} is ready.'.format(client.user)) # Sets prefix for commands (!Command)
    
@client.event 
async def on_member_join(ctx):
    role = discord.utils.get(ctx.guild.roles, name = "Example Role") 
    await ctx.add_roles(role)

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.orange()
    )

    embed.set_author(name='Help')
    embed.add_field(name='.ping', value='Returns Pong!', inline=False)
    embed.add_field(name='.echo', value='Echoes what you say after the command')

    await author.send(embed=embed)

@client.command(pass_context=True)
async def join(ctx):
    try:
        if ctx.message.author.voice:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You're not in a voice channel in order for me to join! \U0001f611")
    except Exception:
        await ctx.send("Already connected to a voice \U0001f61c")
    

@client.command(pass_context=True)
async def leave(ctx):
    voice_client = ctx.voice_client
    if voice_client:
        await voice_client.disconnect(force=True)
        await ctx.message.add_reaction("☑")
    else:
    	await ctx.send("I'm not in a voice channel! \U0001f611")   

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

@client.command()
async def echo(ctx, *args):
    await ctx.send(' '.join(args))

@client.command(pass_context=True)
async def clearme(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    counter = 0
    async for message in channel.history(limit=amount):
        if str(message.author) == "roughhead1#6919":
            counter += 1
            messages.append(message)
    await channel.delete_messages(messages)

def displayembed(tit, description, colour, author, image_url, thumbnail_url, footer):
    embed = discord.Embed(
        title=tit,
        description=description,
        colour=colour
    )

    embed.set_footer(text=footer)
    embed.set_image(url=image_url)
    embed.set_thumbnail(url=thumbnail_url)
    embed.set_author(name=author)
    embed.add_field(name='Field Name', value='Field Value', inline=False)
    embed.add_field(name='Field Name', value='Field Value', inline=True)
    embed.add_field(name='Field Name', value='Field Value', inline=True)

    return embed

@client.command()
async def logout(ctx):
    await client.logout()

@client.command()
async def clearbot(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    counter = 0
    async for message in channel.history(limit=amount):
        if str(message.author) == "T.DJ#4852":
            counter += 1
            messages.append(message)
    await channel.delete_messages(messages)

@client.command(pass_context=True)
async def play(ctx):
# try:
    vc = ctx.voice_client
    print("Playing audio")
    # vc.play(discord.FFmpegPCMAudio('Don Toliver - Thank God.mp3'), after=lambda e: print('done', e))
    vc.play(discord.FFmpegPCMAudio('Don Toliver - Thank God.mp3'), after=lambda : check_queue(ctx.guild.id))
    vc.volume = 100
    vc.is_playing()
# except Exception:
#     await ctx.send("Not connected to a voice channel \U0001f61e")

@client.command(pass_context=True)
async def pause(ctx):
    try:
        voice = ctx.voice_client
        voice.pause()
    except Exception:
        await ctx.send("Not connected to a voice channel \U0001f61e")

@client.command(pass_context=True)
async def stop(ctx):
    try:
        voice = ctx.voice_client
        voice.stop()
    except Exception:
        await ctx.send("Not connected to a voice channel \U0001f61e")

@client.command(pass_context=True)
async def resume(ctx):
    try:
        voice = ctx.voice_client
        voice.resume()
    except Exception:
        await ctx.send("Not connected to a voice channel \U0001f61e")

def check_queue(id):
    vc = ctx.voice_client
    if queues[id] != []:
        song = queues[id].pop(0)
        vc.play(discord.FFmpegPCMAudio(str(song)), after=lambda e: print('done', e))
        vc.is_playing()

    
@client.command(pass_context=True)
async def queue(ctx, *args):
    vc = ctx.voice_client
    guild_id = ctx.guild.id
    songs = [song for i in args]
    if guild_id not in queues:
        queues[guild_id] = []
    for song in songs:
        queues[guild_id].append(song)
    await ctx.send("Song(s) queued")

    for song in songs:
        vc.play(discord.FFmpegPCMAudio(str(song)), after=lambda : check_queue(ctx.guild.id))


client.loop.create_task(change_status())
client.run(TOKEN)
    