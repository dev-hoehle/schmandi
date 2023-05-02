import asyncio
import json
import os
import platform
import sys
from datetime import datetime

import discord
import requests
from colorama import Fore
from discord.ext import commands, tasks

from helpers.general import print_failure_message, print_success_message
from helpers.config import get_config_value, check_config
check_config()


token = get_config_value("Token")
if not token:
    print_failure_message("Token is missing from config.json. Please follow the setup instructions from the README file.")
    sys.exit()
greet = get_config_value("greetmembers")



def clear_console():
    try:
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
    except Exception as e:
        print(f"Error: {e}")


loaded = 0
allcogs = 0


class Bot(commands.Bot):
    def __init__(self, *, intents: discord.Intents):

        super().__init__(command_prefix=commands.when_mentioned_or("$$"), intents=intents)

    async def setup_hook(self):
        global loaded, allcogs
        clear_console()
        print("")
        for filepath in os.listdir('cogs'):
            for filename in os.listdir(f'cogs/{filepath}'):
                if filename.endswith('.py'):
                    filename = filename.replace('.py', '')
                    allcogs += 1
                    try:
                        time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
                        await bot.load_extension(f'cogs.{filepath}.{filename}')
                        print_success_message(f'[{time}] [{Fore.LIGHTCYAN_EX}BOT{Fore.RESET}] [\u2705] Loaded cogs.{filepath}.{filename}')
                        loaded += 1
                    except Exception as error:
                        print_failure_message(f'[{time}] [{Fore.RED}BOT{Fore.RESET}] [\u274C] Failed to load cogs.{filepath}.{filename}: {error}')

        await self.tree.sync()


intents = discord.Intents.all()
intents.presences = True
intents.members = True
bot = Bot(intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle)

    time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    print(f'[{time}] [{Fore.LIGHTCYAN_EX}BOT{Fore.RESET}] Loaded [{loaded}/{allcogs}] cogs')

    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="anditv.it"),)
    print(f'\n[{time}] [{Fore.LIGHTCYAN_EX}BOT{Fore.RESET}] has connected as {bot.user} via discord.py {discord.__version__}')

    bg_task.start()


@bot.event
async def on_member_join(member):
    try:
        if greet:
            await member.create_dm()
            await member.dm_channel.send(f'Welcome **{member.name}** to **{member.guild.name}**!')
    except Exception:
        pass


@tasks.loop(seconds=5)
async def bg_task():
    await bot.wait_until_ready()
    counted_members = set()
    while not bot.is_closed():
        member_count = len(counted_members)
        for guild in bot.guilds:
            for member in guild.members:
                if member.id not in counted_members:
                    counted_members.add(member.id)
                    member_count += 1

        status_list = [
            (discord.Status.dnd, discord.Activity(
                type=discord.ActivityType.watching, name="github.com/anditv21")),
            (discord.Status.dnd, discord.Activity(
                type=discord.ActivityType.watching, name="anditv.it")),
            (discord.Status.dnd, discord.Activity(
                type=discord.ActivityType.watching, name=f"{member_count} users")),
            (discord.Status.dnd, discord.Activity(
                type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers"))
        ]

        if platform.system() == 'Windows':
            status_list[2] = (discord.Status.idle, discord.Activity(
                type=discord.ActivityType.playing, name="development"))
            await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(
                type=discord.ActivityType.playing, name="development"))
            return False

        current_index = 0
        while current_index < len(status_list):
            status, activity = status_list[current_index]
            try:
                await bot.change_presence(status=status, activity=activity)
                await asyncio.sleep(5)
            except discord.HTTPException as e:
                print(f"Error occurred while changing presence: {e}")

            current_index += 1
"""
@bot.event
async def on_message(message):
    print(str(message.content))
"""

bot.run(token=token, log_level=40)
