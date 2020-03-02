import discord
from discord.ext import commands

TOKEN = 'NjgzNzA3NzAyMzM3NDcwNTE0.Xlvejg.95qDunQ-2AhDc2H5g7VfPjkH7ck'

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Bot {} is ready.'.format(client.user))

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

@client.command()
async def echo(ctx, *args):
    await ctx.send(''.join(args))





# @client.event
# async def on_message_delete(message):
#     author = message.author
#     content = message.content
#     channel = message.channel
#     if not author.bot:
#         await message.channel.send('Message "{}" from user {} was deleted'.format(content, author))


client.run(TOKEN)
    