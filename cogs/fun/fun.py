import json
import random
from datetime import datetime

import discord
import requests
from bs4 import BeautifulSoup
from discord import app_commands
from discord.ext import commands

with open("config.json", "r", encoding="UTF-8") as configfile:
    config = json.load(configfile)
    api_key = config["giphy_key"]

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Rolls a virtual dice")
    @app_commands.describe(sides="How many sides do you want?")
    async def roll(self, interaction: discord.Interaction, sides: int):
        if sides < 2:
            embed = discord.Embed(title="The number of sides must be greater than 1!", imestamp=datetime.now(), color=discord.Color.dark_red(),)
            embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        roll = random.randint(1, sides)
        
        embed=discord.Embed(color=0x00fffa)
        embed.add_field(name="Virtual dice", value=f'You rolled a {roll}!', inline=False)
        await interaction.response.send_message(embed=embed)


    @app_commands.command(name='gifsearch', description='Shows you a random gif for your query')
    @app_commands.describe(query="Search query?")
    async def gifsearch(self, interaction: discord.Interaction, *, query: str):
        url = f"https://api.giphy.com/v1/gifs/search?api_key={api_key}&q={query}&limit=1"
        response = requests.get(url).json()
        gif_url = response["data"][0]["images"]["original"]["url"]
        embed = discord.Embed(title=f"Gif for {query}", color=0x00EFDB)
        embed.set_image(url=gif_url)
        embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))
