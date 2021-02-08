import os
from dotenv import load_dotenv
from random import randint
import re
from discord.ext import commands
import discord
from discord import Color
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

# todo make sure role isn't taken yet
@bot.command(name='embark', help='[character name] to embark on the quest!')
async def embark(ctx, name):
    guild = ctx.guild
    await guild.create_role(name=name, color=Color.dark_grey(), mentionable=True, reason='New adventurer')
    role = next(r for r in guild.roles if r.name == name)
    await ctx.author.add_roles(role, reason='New adventurer')
    
    uid = ctx.author.id
    db_manager.add_adventurer(uid, name)
    await ctx.send(f'{name} joins the quest!')

@bot.command(name='add_objective')
@commands.has_role('Inconsistent')
async def add_objective(ctx, name, description):
    db_manager.add_objective(name, description)
    await ctx.send(f'{name} has been added to the list of objectives!')

# todo
@bot.command(name='objectives', help='The current objective')
async def objectives(ctx):
    objectives = db_manager.get_current_objectives()
    await ctx.send(f'Current objectives:\n{objectives}')

@bot.command(name='solve')
@commands.has_role('Inconsistent')
async def solve(ctx, objective_id):
    db_manager.solve_objective(objective_id)
    objective = db_manager.get_objective_by_id(objective_id)
    await ctx.send(f'Congratulations on solving {objective}')

@bot.command(name='add_location')
@commands.has_role('Inconsistent')
async def add_location(ctx, place):
    db_manager.add_location(place)
    await ctx.send(f'The party is now in {place}!')

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

if __name__ == '__main__':
    try:
        bot.run(TOKEN)
    finally:
        #todo remove this line when active
        db_manager.clear_db()
        print('bot shut down')