import click
from secret import *
from _discord.discord import bot, reddit_feed

@click.group()
def cli():
    pass

@click.command()
def web():
    print("Web")

@click.command()
def discord():
    print("Discord")
    if FEED_CHANNEL is not None:
        bot.loop.create_task(reddit_feed())
    bot.run(DISCORD_KEY)

cli.add_command(web)
cli.add_command(discord)

if __name__ == '__main__':
    cli()
