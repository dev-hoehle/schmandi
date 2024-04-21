import base64
import json
import platform
import sys
from helpers.utilFunctions import checkMember
from datetime import datetime
from typing import Literal
from urllib.parse import urlparse

import aiohttp
import cpuinfo
import discord
import psutil
from bs4 import BeautifulSoup
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View

from helpers.general import print_failure_message

sys.dont_write_bytecode = True

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="avatar", description="Shows the avatar of a user")
    @app_commands.describe(member="The member whose avatar you want to view")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        checkedMember = checkMember(interaction=interaction, member=member)

        embed = discord.Embed(
            color=0x00EFDB
        ).set_author(
            name=f"{checkedMember.display_name}'s avatar",
            url=f"https://discord.com/users/{checkedMember.id}",
            icon_url=str(checkedMember.avatar)
        ).set_image(
            url=str(checkedMember.avatar)
        ).set_footer(
            text=f"Requested by {interaction.user.name}",
            icon_url=str(interaction.user.avatar)
        )

        button = Button(style=discord.ButtonStyle.link, label=f"Download {checkedMember.display_name}'s Avatar", url=str(checkedMember.avatar))
        view = View()
        view.add_item(button)

        await interaction.response.send_message(embed=embed, view=view)




    @app_commands.command(name="base64decode", description="Decodes a Base64 string")
    @app_commands.describe(text="What is your encoded text?")
    async def base64decode(self, interaction: discord.Interaction, text: str):
        decoded = base64.b64decode(text).decode("utf-8", "ignore")
        embed = discord.Embed(
            title=f"Your decoded text:\n ||{decoded.__str__()}||",
            color=0x00D9FF
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="base64_encode", description="Base64 encodes a string")
    @app_commands.describe(text="What is the text you want to encode?")
    async def base64_encode(self, interaction: discord.Interaction, *, text: str):
        string_bytes = text.encode("ascii")

        base64_bytes = base64.b64encode(string_bytes)
        base64_string = base64_bytes.decode("ascii")

        embed = discord.Embed(
            title=f"Your encoded text:\n ||{base64_string.__str__()}||",
            color=0x00D9FF
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


    # i was bored
    @app_commands.command(name="yt", description="Download a YouTube video by providing its URL")
    @app_commands.describe(url="Enter the URL of the YouTube video you want to download")
    async def yt(self, interaction: discord.Interaction, url: str):
        try:
            # Parse the URL
            parsed_url = urlparse(url)

            # Check if the URL is valid
            if parsed_url.scheme and parsed_url.netloc:

                # If the URL is a shortened youtu.be link, replace it with the full link
                if parsed_url.netloc == "youtu.be":
                    url = "https://www.youtube.com/watch?v=" + parsed_url.path.lstrip("/")

                # If the URL is a YouTube music link, replace it with the video link
                if parsed_url.netloc == "music.youtube.com":
                    url = "https://www.youtube.com/watch?v=" + parsed_url.path.lstrip("/")

                # Create the video download link and scrape the download page
                download_page_url = "https://10downloader.com/download?v=" + url

                try:
                    async with aiohttp.ClientSession() as session:
                        html_text = await session.get(url=download_page_url)
                        html_text = await html_text.read()
                except:
                    return await interaction.response.send_message("Unable to retrieve download link", ephemeral=True)

                soup = BeautifulSoup(html_text.decode('utf-8'), "html.parser")
                download = soup.find("tbody").find("a", href=True, text="Download")
                if not download:
                    return await interaction.response.send_message("Unable to retrieve download link", ephemeral=True)

                download_url = download["href"]
                thumbnail_url = soup.find("div", {"class": "info"}).find("img")["src"]
                video_title = soup.find("div", {"class": "info"}).find("span", {"class": "title"}).text.strip()

                # Shorten the download link using the TinyURL API
                tinyurl_api_url = "http://tinyurl.com/api-create.php?url=" + download_url  # Renamed link to tinyurl_api_url
                try:
                    async with aiohttp.ClientSession() as session:
                        short_url = await session.get(url=tinyurl_api_url)
                        short_url = await short_url.read()
                except:
                    return await interaction.response.send_message("Unable to shorten download link.", ephemeral=True)

                short_url = short_url.decode('utf-8')  # Decode the byte string to a regular string

                # Create a button
                button = Button(style=discord.ButtonStyle.link, label="Download", url=short_url)

                # Create a view and add the button
                view = View()
                view.add_item(button)

                embed = discord.Embed(
                    title=video_title,
                    color=0xFF0000
                ).set_thumbnail(
                    url=thumbnail_url
                )
                await interaction.response.send_message(embed=embed, ephemeral=True, view=view)
            else:
                return await interaction.response.send_message("The provided url is invalid.", ephemeral=True)

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return await interaction.response.send_message(error_message, ephemeral=True)



    @app_commands.command(name="userinfo", description="Shows information about a user")
    @app_commands.describe(member="About which member do you want to get infos?")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        checkedMember = checkMember(interaction=interaction, member=member)

        user_created_at = checkedMember.created_at.strftime("%b %d, %Y %I:%M %p")
        joined_at = checkedMember.joined_at.strftime("%b %d, %Y %I:%M %p")

        embed = discord.Embed(
            color=checkedMember.color
        ).set_thumbnail(
            url=checkedMember.display_avatar
        ).set_author(
            name=f"{checkedMember.display_name}'s Info",
            icon_url=checkedMember.avatar
        ).add_field(
            name="Name",
            value=f"```{checkedMember.name}```",
            inline=False
        )   .add_field(
            name="Display Name",
            value=f"```{checkedMember.display_name}```",
            inline=False
        ).add_field(
            name="Global Name",
            value=f"```{checkedMember.global_name}```",
            inline=False
        ).add_field(
            name="ID",
            value=f"```{checkedMember.id}```",
            inline=False
        ).add_field(
            name="Creation",
            value=f"```{user_created_at}```",
            inline=False
        ).add_field(
            name="Joined",
            value=f"{joined_at}",
            inline=True
        ).add_field(
            name="Nickname",
            value=f"{checkedMember.nick}",
            inline=True
        ).add_field(
            name="Highest Role",
            value=f"{checkedMember.top_role.mention}",
            inline=True
        )

        button = Button(style=discord.ButtonStyle.link, label=f"Download {checkedMember.display_name}'s Avatar", url=str(checkedMember.avatar))
        button2 = Button(style=discord.ButtonStyle.link, label=f"Download {checkedMember.display_name}'s guild Avatar", url=str(checkedMember.display_avatar))
        view = View()
        view.add_item(button)
        view.add_item(button2)


        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="ping", description="Pong")
    async def ping(self, interaction: discord.Interaction):

        # Calculate the ping in milliseconds
        ping_ms = round(self.bot.latency * 1000)

        if ping_ms <= 50:
            color = 0x44FF44
        elif ping_ms <= 100:
            color = 0xFFD000
        elif ping_ms <= 200:
            color = 0xFF6600
        else:
            color = 0x990000

        embed = discord.Embed(title="PING", description=f"Pong! The ping is **{ping_ms}** milliseconds!", color=color,)

        await interaction.response.send_message(embed=embed)



    @app_commands.command(name="botinfo", description="Shows information about the bot.")
    async def botinfo(self, interaction: discord.Interaction):
        name = self.bot.user
        id = self.bot.user.id

        # Get information about the Python version, OS, CPU, and RAM usage
        python_version = platform.python_version()
        os_version = platform.system()
        cpu_name = cpuinfo.get_cpu_info()['brand_raw']
        ram_usage = psutil.virtual_memory().percent

        info = f"Bot-Name: {name} ({id}) \nPython: {python_version}\nDiscord.py: {discord.__version__}\nOS: {os_version}\nCPU: {cpu_name}\nRAM: {ram_usage} %"

        embed = discord.Embed(
            color=0x00D9FF
        ).add_field(
            name="Bot Info",
            value=f"```{info}```",
            inline=False
        ).set_footer(
            text=f"Requested by {interaction.user.name}",
            icon_url=interaction.user.display_avatar
        )
        await interaction.response.send_message(embed=embed)


    @app_commands.command(name='discordstatus', description="Shows you the discord server status")
    async def discordstatus(self, interaction: discord.Interaction):
        try:
            # Get the server status from the Discord status API
            async with aiohttp.ClientSession() as session:
                response = await session.get(url="https://discordstatus.com/api/v2/summary.json")
                data = json.loads(await response.text())

                if response.status != 200:
                    raise ValueError(f"Unexpected HTTP status code: {response.status}")

            # Extract the component information from the API response
            components = [
                {
                    "name": component["name"],
                    "value": component["status"].capitalize(),
                    "inline": True
                } for component in data["components"]
            ]

            embed = discord.Embed(
                title=data["status"]["description"],
                description=f"[Discord Status](https://discordstatus.com/)\n **Current Incident:**\n {data['status']['indicator']}",
                color=0x00D9FF,
                timestamp=datetime.now()
            ).set_thumbnail(
                url="https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png"
            )
            for component in components:
                embed.add_field(name=component["name"], value=component["value"], inline=component["inline"])
            await interaction.response.send_message(embed=embed)
        except ValueError as e:
            embed = discord.Embed(
                title="Error while retrieving discord status",
                description=str(e),
                color=discord.Color.dark_red(),
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message("Error: " + str(e))



async def setup(bot):
    await bot.add_cog(Util(bot))