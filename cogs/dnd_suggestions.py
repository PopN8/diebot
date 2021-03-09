import os
from dotenv import load_dotenv
from random import randint
from random import choice
import re
from discord.ext import commands
import discord
from discord import Color
import time
from db import db_exceptions, db_manager
from db.db_manager import PromptIndexError

class DndSuggestions(commands.Cog, name='?DnDSuggestionCommands'):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = '?'

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name='add_prompt', brief='Add a prompt', help='?[prompt] as a sentence to create a prompt. Use # to indicate a choice')
    @commands.guild_only()
    async def add_prompt(self, ctx, *prompt):
        prompt = ' '.join(prompt)
        if ctx.prefix == '?':
            max_index = prompt.count('#') - 1
            prompt = prompt.replace('#', '{}')
            db_manager.add_prompt(max_index, prompt)
            await ctx.send(f'Prompt successfully added!\n{prompt}')

    @commands.command(name='prompt', brief='Show a specific prompt', help='?[prompt_id] to show the selected prompt and choices associated with it')
    @commands.guild_only()
    async def prompt(self, ctx, prompt_id: int, choice_filter=''):
        if ctx.prefix == '?':
            prompt_ret = db_manager.get_prompt(prompt_id)
            embed = discord.Embed(
                title = prompt_ret.prompt,
                description = f'Index options: {[i for i in range(prompt_ret.max_index + 1)]}'
            )
            if choice_filter == '':
                get_all = True
            elif choice_filter == 'a':
                get_approved_only = True
            elif choice_filter == 'n':
                get_approved_only = False
            else:
                await ctx.send('Not a valid filter, sending all choices')
                get_all = True
            for i, expression in enumerate(prompt_ret.expressions):
                if expression.choices:
                    embed.add_field(
                        name=f'Choice #{i}', value='\n'.join(
                            [choice.choice for choice in expression.choices if get_all or (get_approved_only and choice.approved)]
                        )
                    )

            await ctx.send(embed=embed)

    @commands.command(name='prompts', brief='Show all prompts', help='?[] Show all current prompts')
    @commands.guild_only()
    async def prompts(self, ctx, choice_filter=''):
        if ctx.prefix == '?':
            if choice_filter == '':
                prompt_lst = db_manager.get_all_prompts()
            elif choice_filter == 'a':
                prompt_lst = db_manager.get_accepted_prompts()
            elif choice_filter == 'n':
                prompt_lst = db_manager.get_pending_prompts()
            else:
                await ctx.send('Not a valid filter, sending all prompts')
                prompt_lst = db_manager.get_all_prompts()
            page_no = 1
            page_count = 1
            embed = discord.Embed(
                title = 'Prompts:',
                description = f'Page #{page_no} of {page_count}'
            )
            for prompt in prompt_lst:
                embed.add_field(name=f'Prompt id: {prompt.prompt_id}', value=prompt.prompt, inline=False)

            await ctx.send(embed=embed)

    # TODO use the emotes
    @commands.command(name='vote_prompt', hidden=True, brief='Vote on the prompt', help='?[prompt id] Vote with reaction to see if prompt is to be approved.')
    @commands.guild_only()
    @commands.has_role('Inconsistent')
    async def vote_prompt(self, ctx, prompt_id: int):
        if ctx.prefix == '?':
            prompt_ret = db_manager.get_prompt(prompt_id)
            embed = discord.Embed(
                title = 'Vote with 👍 and 👎 to decide whether the prompt should be used!',
                description = prompt_ret.prompt
            )
            await ctx.send(embed=embed)

    @commands.command(name='add_choice', brief='Add a chocie', help='?[prompt id] [choice index] [choice] add a choice for the selected prompt')
    @commands.guild_only()
    async def add_choice(self, ctx, prompt_id: int, choice_index: int, *choice):
        choice = ' '.join(choice)
        if ctx.prefix == '?':
            try:
                db_manager.add_choice(prompt_id, choice_index, choice)
            except PromptIndexError as e:
                ctx.send(str(e))
            await ctx.send(f'Choice successfully added!\n{choice}')

    # TODO use the emotes
    @commands.command(name='vote_choice', hidden=True, brief='Vote on the choice', help='?[prompt id] [choice id] Vote with reaction to see if choice is to be approved.')
    @commands.guild_only()
    @commands.has_role('Inconsistent')
    async def vote_choice(self, ctx, prompt_id: int, choice_id:int):
        if ctx.prefix == '?':
            prompt_ret = db_manager.get_prompt(prompt_id)
            embed = discord.Embed(
                title='Vote with 👍 and 👎 to decide whether the choice should be used!',
                description=prompt_ret.prompt
            )
            prev = prompt_ret.max_index
            embed.add_field(name='Usage example', value=prompt.format(*['{}']*prev, choice, *['{}']*15))
            await ctx.send(embed=embed)

    @commands.command(name='test_prompt', brief='Test a prompt', help='?[prompt id] Test the selected prompt with available choices.')
    @commands.guild_only()
    async def test_prompt(self, ctx, prompt_id: int):
        if ctx.prefix == '?':
            prompt_ret = db_manager.get_prompt(prompt_id)
            choices = []
            for expression in prompt_ret.expressions:
                if expression.choices:
                    choices.append(choice([choice.choice for choice in expression.choices]))
                else:
                    choices.append('{}')

            embed = discord.Embed(
                title=f'Testing prompt #{prompt_id}',
                description=prompt_ret.prompt.format(*choices)
            )
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(DndSuggestions(bot))