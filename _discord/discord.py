import asyncio
import sys
from secret import *
import discord
from discord.ext import commands
from reddit import reddit
import time

rs = reddit.RedditSession(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    password=REDDIT_PASSWORD,
    username=REDDIT_USERNAME,
    user_agent=REDDIT_USER_AGENT
)
bot = commands.Bot(command_prefix='%')
# TODO: Put this in a database.
"""
badwords = []
"""

@bot.command(name='ping', pass_context=True)
async def ping(ctx):
    """
    Ping command for testing that the bot is online.
    """
    await ctx.send('pong')

@bot.command(name='notes')
async def notes(ctx, user):
    """
    Get the usernotes from moderator toolbox for a user.
    """
    usernotes = rs.get_usernotes(SUBREDDIT)
    if user not in usernotes:
        await ctx.send("No notes found for {}.".format(user))
    else:
        print(usernotes)
        await ctx.send("{}".format(usernotes[user]))

# TODO: Connect this to a database.
"""
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
"""

async def reddit_feed():
    await bot.wait_until_ready()
    start_time = time.time()
    #submissions = rs.stream(SUBREDDITS).submissions(pause_after=0)
    feed = reddit.SubmissionFeed(SUBREDDITS, 60)
    feed_chan = bot.get_channel(FEED_CHANNEL)
    while not bot.is_closed():
        for sub in feed.submission():
            embed = discord.Embed(
                title=sub.title,
                description="New post in {}".format(sub.subreddit),
                url=sub.url,
                color=0x00ff00
            )
            # TODO: This is a shortcut.
            # Refine this for better support of other image formats.
            # Consider using thumbnails as well if the post is a link.
            # Basically just make this richer.
            if 'png' in sub.link or 'jpg' in sub.link:
                embed = embed.set_image(url=sub.link)
            embed = embed.set_author(
                name=sub.author,
                url="https://reddit.com{}".format(sub.author)
            )
            await feed_chan.send(embed=embed)
        await asyncio.sleep(60)

@bot.event
async def on_ready():
    print("Running...")

