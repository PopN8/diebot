import os
from dotenv import load_dotenv
from random import randint
import re
from discord.ext import commands
import discord
import time
from db import db_manager

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('We have logged in as {bot.user}')
    db_manager.update_schemes()
    print('Database schemes updated')


@bot.command(name='origin')
async def origin(ctx):
    await ctx.send('A tale as old as time...')
    time.sleep(2.5)
    await ctx.send('https://twitter.com/PopNEight/status/1333487555556347904?s=20')

# todo
@bot.command(name='intro')
async def intro(ctx):
    await ctx.send('Welcome, travelers!')

# todo
@bot.command(name='embark', help='[character name] to embark on the quest!')
async def embark(ctx, name):
    uid = ctx.author[0].id
    db_manager.add_adventurer(uid, name)
    await ctx.send(f'{name} joins the quest!')

# todo
@bot.command(name='objectives', help='The current objective')
async def objectives(ctx):
    objectives = db_manager.get_current_objectives()
    await ctx.send(f'Current objectives:\n{objectives}')

# todo
@bot.command(name='location', help='The current party location')
async def location(ctx):
    location = db_manager.get_current_location()
    await ctx.send(f'Current location:\n{location}')

@bot.command(name='roll', help='[die] written as number of dice, d, die count. Ex: 2d20 will roll 2 20-sided dice.')
async def roll(ctx, *dice):
    for die in dice:
        match = re.compile('^\d*d\d*$')
        if not match.match(die):
            await ctx.send('You fool! The dice will not respond to such mistreatment!')
            continue
        count, value = die.split('d')
        for c in range(int(count)):
            await ctx.send(f'die {c+1}: {randint(1, int(value))}')

try:
    bot.run(TOKEN)
finally:
    #todo remove this line when active
    db_manager.clear_db()
    print('bot shut down')