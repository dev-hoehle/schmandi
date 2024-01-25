import random
import sys
from datetime import datetime
from typing import Literal

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from helpers.config import get_config_value
from helpers.general import print_failure_message

sys.dont_write_bytecode = True

api_key = get_config_value("tenor_key")
api_name = get_config_value("tenor_name")

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Rolls a virtual dice")
    @app_commands.describe(sides="How many sides do you want?")
    async def roll(self, interaction: discord.Interaction, sides: int):
        if sides < 2:
            embed = discord.Embed(
                title="The number of sides must be greater than 1!",
                imestamp=datetime.now(),
                color=discord.Color.dark_red()
            ).set_footer(
                text=interaction.guild.name,
                icon_url=interaction.guild.icon.url
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        roll = random.randint(1, sides)

        embed=discord.Embed(
            color=0x00fffa
        ).add_field(
            name="Virtual dice",
            value=f'You rolled a {roll}!',
            inline=False
        )
        await interaction.response.send_message(embed=embed)



    @app_commands.command(name='gifsearch', description='Shows you a random gif for your query')
    @app_commands.describe(query="Search query?")
    async def gifsearch(self, interaction: discord.Interaction, *, query: str):

        if not api_key:
            return await interaction.response.send_message("Tenor API key is missing from config.json. Please follow the setup instructions from the README file.", ephemeral=True)
        url = f"https://tenor.googleapis.com/v2/search?q={query}&client_key={api_name}&key={api_key}&limit=50"

        # send a request to the Tenor API and get the response in JSON format
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=url)
            response = await response.json()

        # choose a random gif from the list of gifs returned by the API
        gif_url = random.choice(response["results"])["media_formats"]["tinygif"]["url"]


        embed = discord.Embed(
            title=f"Gif for {query}",
            color=0x00EFDB
        ).set_image(
            url=gif_url
        ).set_footer(
            text=f"Requested by {interaction.user.name}",
            icon_url=interaction.user.avatar
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='bombastic_side_eye', description='Bombastic side eye')
    async def bombastic_side_eye(self, interaction: discord.Interaction):
        if not api_key:
            await interaction.response.send_message("Tenor API key is missing from config.json. Please follow the setup instructions from the README file.", ephemeral=True)
            return

        cat_url = f"https://tenor.googleapis.com/v2/search?q=side+eye+cat&client_key={api_name}&key={api_key}&limit=50"
        dog_url = f"https://tenor.googleapis.com/v2/search?q=side+eye+dog&client_key={api_name}&key={api_key}&limit=50"

        async with aiohttp.ClientSession() as session:
            cat_response = await session.get(url=cat_url)
            cat_response = await cat_response.json()

            dog_response = await session.get(url=dog_url)
            dog_response = await dog_response.json()

        combined_results = cat_response["results"] + dog_response["results"]

        # Access the GIF URL from the "tinygif" format
        gif_url = random.choice(combined_results)["media_formats"]["tinygif"]["url"]

        embed = discord.Embed(
            title="Bombastic side eye",
            color=0x00EFDB
        ).set_image(
            url=gif_url
        ).set_footer(
            text=f"Requested by {interaction.user.name}",
            icon_url=interaction.user.avatar
        )
        await interaction.response.send_message(embed=embed)





    @app_commands.command(name="fact", description="Shows you a useless fact")
    @app_commands.describe(language="In which language should your useless fact be shown?")
    @app_commands.describe(visibility="Do you want the fact to be visible to everyone?")
    async def fact(self, interaction: discord.Interaction, language: Literal["English", "German"] = "English", visibility: Literal["true", "false"] = "false"):
        try:
            # Mapping of languages to codes for the API
            language_codes = {"English": "en", "German": "de"}

            visibility = {"true": True, "false": False}.get(visibility, False)

            code = language_codes.get(language)
            if not code:
                code = "en"


            url = f"https://uselessfacts.jsph.pl/random.json?language={code}"
            factembed = discord.Embed(
                timestamp=datetime.now(),
                color=discord.Color.dark_red()
            ).set_footer(
                text=interaction.guild.name,
                icon_url=interaction.guild.icon.url
            )

            try:
                # Make a GET request to the API and check the response status code
                async with aiohttp.ClientSession() as session:
                    response = await session.get(url=url)

                    response.raise_for_status()  # Raise an exception for non-200 status codes

                    # Parse the JSON response and get the useless fact
                    data = await response.json()
                    fact = data["text"]
                    factembed.add_field(name="Useless Fact:", value=fact)

                    ephemeral = visibility == False  # Set ephemeral to True only if visibility is "false"

                    await interaction.response.send_message(embed=factembed, ephemeral=ephemeral)

            except:
                factembed.add_field(name="Error:", value="Failed to parse response as JSON.")
                await interaction.response.send_message(embed=factembed, ephemeral=True)
        except Exception as e:
            print_failure_message(e)



async def setup(bot):
    await bot.add_cog(Fun(bot))
