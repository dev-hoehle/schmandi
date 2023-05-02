import os
import platform
import discord
from discord.ext import commands
from datetime import datetime

from colorama import Fore

def clear_console():
    try:
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
    except Exception as e:
        print(f"Error: {e}")


def print_success_message(text):
    time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    print(f"[{time}] [{Fore.LIGHTCYAN_EX}BOT{Fore.RESET}] [\u2705] {text}")
    
def print_failure_message(text):
    time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    print(f"[{time}] [{Fore.RED}BOT{Fore.RESET}] [\u274C] {text}")

