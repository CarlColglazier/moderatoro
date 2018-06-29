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
badwords = []

@bot.command(name='ping')
async def ping(ctx):
    """
    Ping command for testing that the bot is online.
    """
    await ctx.send('pong')

@bot.command(name='notes')
async def ntoes(ctx, user):
    usernotes = rs.get_usernotes(SUBREDDIT)
    if user not in usernotes:
        await ctx.send("No notes found for {}.".format(user))
    else:
        print(usernotes)
        await ctx.send("{}".format(usernotes[user]))

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

async def reddit_feed():
    await bot.wait_until_ready()
    start_time = time.time()
    submissions = rs.stream(SUBREDDITS).submissions(pause_after=0)
    feed_chan = bot.get_channel(FEED_CHANNEL)
    while not bot.is_closed():
        submission = next(submissions)
        if submission is None:
            print("Waiting...")
            await asyncio.sleep(15)
        elif submission.created_utc > start_time:
            embed = discord.Embed(
                title=submission.title,
                description="New post in /r/{}".format(submission.subreddit),
                url=submission.shortlink,
                color=0x00ff00
            )
            # TODO: This is a shortcut.
            if 'png' in submission.url or 'jpg' in submission.url:
                embed = embed.set_image(url=submission.url)
            embed = embed.set_author(
                name=submission.author,
                url="https://reddit.com/u/{}".format(submission.author)
            )
            await feed_chan.send(embed=embed)

@bot.event
async def on_ready():
    print("Running...")

