import json
import random
from datetime import datetime
from typing import Literal

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
        # construct the Giphy API URL
        url = f"https://api.giphy.com/v1/gifs/search?api_key={api_key}&q={query}&limit=15"
        
        # send a request to the Giphy API and get the response in JSON format
        response = requests.get(url).json()
        
        # choose a random gif from the list of gifs returned by the API
        gif_url = random.choice(response["data"])["images"]["original"]["url"]
        

        embed = discord.Embed(title=f"Gif for {query}", color=0x00EFDB)
        embed.set_image(url=gif_url)
        embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar)
        
        await interaction.response.send_message(embed=embed)



    @app_commands.command(name="fact", description="Shows you a useless fact")
    @app_commands.describe(language="In which language should your useless fact be shown?")
    async def fact(self, interaction: discord.Interaction, language: Literal["English", "German"] = "English"):
        try:
            # Mapping of languages to codes for the API
            language_codes = {"English": "en", "German": "de"}
            code = language_codes.get(language)
            if not code:
                await interaction.response.send_message("Sorry, that language is not supported.", ephemeral=True)
                return

            url = f"https://uselessfacts.jsph.pl/random.json?language={code}"
            factembed = discord.Embed(timestamp=datetime.now(), color=discord.Color.dark_red(
            )).set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)

            try:
                # Make a GET request to the API and check the response status code
                response = requests.get(url)
                if response.status_code != 200:
                    factembed.add_field(name="Error Code:",
                                        value=response.status_code)
                    await interaction.response.send_message(embed=factembed, ephemeral=True)
                    return
                
                # Parse the JSON response and get the useless fact
                data = response.json()
                fact = data["text"]
                factembed.add_field(name="Useless Fact:", value=fact)
                await interaction.response.send_message(embed=factembed, ephemeral=True)
            except requests.exceptions.RequestException as e:
                factembed.add_field(name="Error:", value=str(e))
                await interaction.response.send_message(embed=factembed, ephemeral=True)
            except ValueError:
                factembed.add_field(
                    name="Error:", value="Failed to parse response as JSON.")
                await interaction.response.send_message(embed=factembed, ephemeral=True)
        except Exception as e:
            print(e)
            
async def setup(bot):
    await bot.add_cog(Fun(bot))
