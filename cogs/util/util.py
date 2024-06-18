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
from discord.ui import Button, View

from helpers.general import print_failure_message
from helpers.util import check_member, isDMChannel

sys.dont_write_bytecode = True

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="avatar", description="Shows the avatar of a user")
    @app_commands.describe(member="The member whose avatar you want to view")
    async def avatar(self, interaction: discord.Interaction, member: discord.User = None):
        target_member = check_member(interaction=interaction, member=member)
        embed = discord.Embed(
            color=0x00EFDB
        ).set_author(
            name=f"{target_member.display_name}'s avatar",
            url=f"https://discord.com/users/{target_member.id}",
            icon_url=str(target_member.avatar)
        ).set_image(
            url=str(target_member.avatar)
        ).set_footer(
            text=f"Requested by {interaction.user.name}",
            icon_url=str(interaction.user.avatar)
        )

        button = Button(style=discord.ButtonStyle.link, label=f"Download {target_member.display_name}'s Avatar", url=str(target_member.avatar))
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


    # @app_commands.command(name="yt", description="Download a YouTube video by providing its URL")
    # @app_commands.describe(url="Enter the URL of the YouTube video you want to download")
    # async def yt(self, interaction: discord.Interaction, url: str):
    #     await interaction.response.defer(ephemeral=True, thinking=True)
    #     try:
    #         # Parse the URL
    #         parsed_url = urlparse(url)

    #         # Check if the URL is valid
    #         if parsed_url.scheme and parsed_url.netloc:

    #             # If the URL is a shortened youtu.be or music link, replace it with the full video link
    #             if parsed_url.netloc == "youtu.be":
    #                 url = "https://www.youtube.com/watch?v=" + parsed_url.path.lstrip("/")
    #             if parsed_url.netloc == "music.youtube.com":
    #                 url = "https://www.youtube.com/watch?v=" + parsed_url.path.lstrip("/")
    #             download_page_url = "https://10downloader.com/download?v=" + url

    #             try:
    #                 async with aiohttp.ClientSession() as session:
    #                     html_text = await session.get(url=download_page_url)
    #                     html_text = await html_text.read()
    #             except:
    #                 return await interaction.response.send_message("Unable to retrieve download link", ephemeral=True)

    #             soup = BeautifulSoup(html_text.decode('utf-8'), "html.parser")
    #             download = soup.find("tbody").find("a", href=True, text="Download")
    #             if not download:
    #                 return await interaction.response.send_message("Unable to retrieve download link", ephemeral=True)

    #             download_url = download["href"]
    #             thumbnail_url = soup.find("div", {"class": "info"}).find("img")["src"]
    #             video_title = soup.find("div", {"class": "info"}).find("span", {"class": "title"}).text.strip()

    #             # Shorten the download link using the TinyURL API
    #             tinyurl_api_url = "http://tinyurl.com/api-create.php?url=" + download_url
    #             try:
    #                 async with aiohttp.ClientSession() as session:
    #                     short_url = await session.get(url=tinyurl_api_url)
    #                     short_url = await short_url.read()
    #             except:
    #                 return await interaction.response.send_message("Unable to shorten download link.", ephemeral=True)

    #             short_url = short_url.decode('utf-8')  # Decode the byte string to a regular string

    #             # Create a button
    #             button = Button(style=discord.ButtonStyle.link, label="Download", url=short_url)

    #             # Create a view and add the button
    #             view = View()
    #             view.add_item(button)

    #             embed = discord.Embed(
    #                 title=video_title,
    #                 color=0xFF0000
    #             ).set_thumbnail(
    #                 url=thumbnail_url
    #             )
    #             #await interaction.response.send_message(embed=embed, ephemeral=True, view=view)
    #             await interaction.followup.send(embed=embed, ephemeral=True, view=view)
    #         else:
    #             #return await interaction.response.send_message("The provided url is invalid.", ephemeral=True)
    #             return await interaction.followup.send("The provided url is invalid.", ephemeral=True)

    #     except Exception as e:
    #         error_message = f"An unexpected error occurred: {str(e)}"
    #         return await interaction.response.send_message(error_message, ephemeral=True)



    async def userinfo(self, interaction: discord.Interaction, member: discord.User = None):
        target_member = check_member(interaction=interaction, member=member)

        user_created_at = target_member.created_at.strftime("%b %d, %Y %I:%M %p")

        embed = discord.Embed(
            color=target_member.color
        ).set_thumbnail(
            url=target_member.display_avatar.url
        ).set_author(
            name=f"{target_member.display_name}'s Info",
            icon_url=target_member.avatar.url if target_member.avatar else ""
        ).add_field(
            name="Name",
            value=f"```{target_member.name}```",
            inline=False
        ).add_field(
            name="Global Name",
            value=f"```{target_member.global_name}```",
            inline=False
        ).add_field(
            name="ID",
            value=f"```{target_member.id}```",
            inline=False
        ).add_field(
            name="Creation",
            value=f"```{user_created_at}```",
            inline=False
        )

        view = View()

        # Add server-specific fields if not in DM
        if not isDMChannel(interaction):
            joined_at = target_member.joined_at.strftime("%b %d, %Y %I:%M %p")
            embed.add_field(
                name="Display Name",
                value=f"```{target_member.display_name}```",
                inline=False
            ).add_field(
                name="Joined",
                value=f"{joined_at}",
                inline=True
            ).add_field(
                name="Highest Role",
                value=f"{target_member.top_role.mention}",
                inline=True
            )

            if target_member.display_avatar:
                button2 = Button(style=discord.ButtonStyle.link, label=f"Download {target_member.display_name}'s guild Avatar", url=str(target_member.display_avatar.url))
                view.add_item(button2)

        if target_member.avatar:
            button = Button(style=discord.ButtonStyle.link, label=f"Download {target_member.display_name}'s Avatar", url=str(target_member.avatar.url))
            view.add_item(button)

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


async def setup(bot):
    await bot.add_cog(Util(bot))