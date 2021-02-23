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

class Dnd(commands.Cog, name='!DnDCommands'):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = '!'

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name='origin', help='![] Bot idea origin')
    @commands.guild_only()
    async def origin(self, ctx):
        if ctx.prefix == '!':
            await ctx.send('A tale as old as time...')
            time.sleep(2.5)
            await ctx.send('https://twitter.com/PopNEight/status/1333487555556347904?s=20')

    # todo
    @commands.command(name='intro', help='![]Quest introduction')
    @commands.guild_only()
    async def intro(self, ctx):
        if ctx.prefix == '!':
            await ctx.send('Welcome, travelers!')

    # todo make sure role isn't taken yet
    @commands.command(name='embark', help='![character name] to embark on the quest!')
    @commands.guild_only()
    async def embark(self, ctx, *name):
        if ctx.prefix == '!':
            name = ' '.join(name)
            guild = ctx.guild
            await guild.create_role(name=name, color=Color.dark_grey(), mentionable=True, reason='New adventurer')
            role = next(r for r in guild.roles if r.name == name)
            await ctx.author.add_roles(role, reason='New adventurer')
            
            uid = ctx.author.id
            db_manager.add_adventurer(uid, name)
            await ctx.send(f'{name} joins the quest!')

    @commands.command(name='add_objective', hidden=True, help='![name] [description] Adds an objective to the quest')
    @commands.has_role('Inconsistent')
    @commands.guild_only()
    async def add_objective(self, ctx, name:str, *description):
        if ctx.prefix == '!':
            description = ' '.join(description)
            db_manager.add_objective(name, description)
            await ctx.send(f'{name} has been added to the list of objectives!')

    # todo
    @commands.command(name='objectives', help='![] The current objective')
    @commands.guild_only()
    async def objectives(self, ctx):
        if ctx.prefix == '!':
            objectives = db_manager.get_current_objectives()
            await ctx.send(f'Current objectives:\n{objectives}')

    @commands.command(name='solve', hidden=True, help='![objective id] Solve an objective')
    @commands.has_role('Inconsistent')
    @commands.guild_only()
    async def solve(self, ctx, objective_id: int):
        if ctx.prefix == '!':
            db_manager.solve_objective(objective_id)
            objective = db_manager.get_objective_by_id(objective_id)
            await ctx.send(f'Congratulations on solving {objective}')

    @commands.command(name='add_location', hidden=True, help='![place] Adds a new location')
    @commands.has_role('Inconsistent')
    @commands.guild_only()
    async def add_location(self, ctx, place: str):
        if ctx.prefix == '!':
            db_manager.add_location(place)
            await ctx.send(f'The party is now in {place}!')

    # todo
    @commands.command(name='location', help='![] The current party location')
    @commands.guild_only()
    async def location(self, ctx):
        if ctx.prefix == '!':
            location = db_manager.get_current_location()
            await ctx.send(f'Current location:\n{location}')

    @commands.command(name='roll', help='![die] Written as number of dice, d, die count. Ex: 2d20 will roll 2 20-sided dice.')
    @commands.guild_only()
    async def roll(self, ctx, *dice):
        if ctx.prefix == '!':
            gay = False
            rolls = []
            total_count = 0
            for die in dice:
                if die == 'gay':
                    gay = True
                    continue
                match = re.compile('^\d*d\d*$')
                if not match.match(die):
                    await ctx.send('You fool! The dice will not respond to such mistreatment!')
                    return
                roll = die.split('d')
                roll = (int(roll[0]), int(roll[1]))
                if roll[0] <= 0 or roll[1] <= 0:
                    await ctx.send('Are you even trying?')
                    return
                total_count += roll[0]
                if total_count > 7:
                    await ctx.send('The dice think you stink')
                    return
                rolls.append(roll)

            for count, value in rolls:
                for c in range(int(count)):
                    embed = discord.Embed(
                        title=f'die {c+1}',
                        description=f'A die has been cast...',
                        color=randint(0, 16777216) if gay else 0
                    )
                    embed.add_field(name='Result', value=randint(1, int(value)))
                    await ctx.send(embed=embed)
    

def setup(bot):
    bot.add_cog(Dnd(bot))