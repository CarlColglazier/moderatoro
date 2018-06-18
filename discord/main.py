import sys
sys.path.append("..")
from secret import *
from discord.ext import commands

bot = commands.Bot(command_prefix='%')
# TODO: Put this in a database.
badwords = []

@bot.command(name='ping')
async def ping(ctx):
    """
    Ping command for testing that the bot is online.
    """
    await ctx.send('pong')

@bot.command(name='badword')
async def badword(ctx, command, word):
    if command == 'list':
        await ctx.send("Bad words: {}".format(', '.join(badwords)))
    elif command == 'add':
        if word in badwords:
            await ctx.send("{} is already in the list of bad words.".format(word))
        else:
            badwords.append(word)
            await ctx.send("{} added to the list of bad words.".format(word))
    elif command == 'remove':
        if word in badwords:
            badwords.remove(word)
            await ctx.send("{} removed from the list of bad words.".format(word))
        else:
            await ctx.send("{} wasn't found in the list of bad words.".format(word))

        
@bot.event
async def on_ready():
    print("Running...")

bot.run(DISCORD_KEY)
