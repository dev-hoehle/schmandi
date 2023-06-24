import base64
import json
import platform
import sys
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

from helpers.general import print_failure_message

sys.dont_write_bytecode = True

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="avatar", description="Shows the avatar of a user")
    @app_commands.describe(member="The member whose avatar you want to view")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user

        embed = discord.Embed(
            title=f"Download {member.name}'s Avatar", 
            url=member.
            avatar,
            color=0x00EFDB
        ).set_author(
            name=f"{member.name}'s avatar",
            url=f"https://discord.com/users/{member.id}", 
            icon_url=member.avatar
        ).set_image(
            url=member.avatar
        ).set_footer(
            text=f"Requested by {interaction.user.name}",
            icon_url=interaction.user.avatar
        )
        await interaction.response.send_message(embed=embed)


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
        # Parse the URL
        parsed_url = urlparse(url)

        # Check if the URL is valid
        if parsed_url.scheme and parsed_url.netloc:
            # If the URL is a shortened youtu.be link, replace it with the full link
            if parsed_url.netloc == "youtu.be":
                url = "https://www.youtube.com/watch?v=" + parsed_url.path.lstrip("/")

            # Create the video download link and scrape the download page
            vgm_url = "https://10downloader.com/download?v=" + url
            try:
                async with aiohttp.ClientSession() as session:
                    html_text = await session.get(url=vgm_url)
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
            link = "http://tinyurl.com/api-create.php?url=" + download_url
            try:
                async with aiohttp.ClientSession() as session:
                    short_url = await session.get(url=link)
                    short_url = await short_url.read()
            except:
                return await interaction.response.send_message("Unable to shorten download link", ephemeral=True)

            short_url = short_url.decode('utf-8')  # Decode the byte string to regular string

            embed = discord.Embed(
                title=video_title,
                color=0xFF0000
            ).set_thumbnail(
                url=thumbnail_url
            ).add_field(
                name="Download",
                value=f"[Click here]({short_url})"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)




    @app_commands.command(name="userinfo", description="Shows information about a user")
    @app_commands.describe(member="About which member do you want to get infos?")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user

        user_created_at = member.created_at.strftime("%b %d, %Y %I:%M %p")
        joined_at = member.joined_at.strftime("%b %d, %Y %I:%M %p")

        embed = discord.Embed(
            color=member.color
        ).set_thumbnail(
            url=member.avatar
        ).set_author(
            name=f"{member.name}'s Info",
            icon_url=member.avatar
        ).add_field(
            name="Tag",
            value=f"```{member.name}```",
            inline=False
        ).add_field(
            name="ID",
            value=f"```{member.id}```",
            inline=False
        ).add_field(
            name="Creation",
            value=f"```{user_created_at}```",
            inline=False
        ).add_field(
            name="Avatar",
            value=f"[Click here]({member.avatar})",
            inline=False
        ).add_field(
            name="Joined",
            value=f"{joined_at}",
            inline=True
        ).add_field(
            name="Nickname",
            value=f"{member.nick}",
            inline=True
        ).add_field(
            name="Highest Role",
            value=f"{member.top_role.mention}",
            inline=True
        )
        await interaction.response.send_message(embed=embed, ephemeral=False)

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
            icon_url=interaction.user.avatar
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