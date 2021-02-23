import os
from dotenv import load_dotenv
from random import randint
import re
from discord.ext import commands
import discord
from discord import Color
import time
from db import db_exceptions, db_manager
from db.db_manager import PromptIndexError

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

initial_extensions = [
    'cogs.owner',
    'cogs.dnd',
    'cogs.dnd_suggestions'
]

bot = commands.Bot(command_prefix=('!', '?', '.'))

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    db_manager.update_schemes()
    print('Database schemes updated')
    await bot.change_presence(activity=discord.Game(name='Testing', type=1))

@bot.command(name='testme')
async def testme(ctx):
    await ctx.send('Please test my ? commands')


if __name__ == '__main__':
    try:
        for extension in initial_extensions:
            bot.load_extension(extension)

        bot.run(TOKEN, bot=True)
    finally:
        #todo remove this line when active
        db_manager.clear_db()
        print('bot shut down')