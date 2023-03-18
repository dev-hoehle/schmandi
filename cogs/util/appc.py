import base64
import json
from datetime import datetime

import discord
import requests
from discord import app_commands
from discord.ext import commands


class util_apps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commands = [
            ("Get Message ID", self.get_message_id),
            ("Get avatar", self.getavatar),
            ("User Info", self.userinfo),
            ("Encode base64", self.base64encode),
            ("Decode base64", self.base64decode)
        ]
        self.create_context_menus()

    def create_context_menus(self):
        # Loop over the list of commands and create a context menu for each one
        for name, callback in self.commands:
            menu = app_commands.ContextMenu(name=name, callback=callback)
            # Add the context menu to the application command tree
            self.bot.tree.add_command(menu)

    async def get_message_id(self, interaction: discord.Interaction, message: discord.Message) -> None:
        await interaction.response.send_message(message.id, ephemeral=True)

    async def getavatar(self, interaction: discord.Interaction, member: discord.Member = None) -> None:
        if member is None:
            member = interaction.user
        avatar = member.avatar
        embed = discord.Embed(title=f"Download {member.name}'s Avatar", url=avatar, color=0x00EFDB,)
        embed.set_author(name=f"{member.name}'s avatar", url=f"https://discord.com/users/{member.id}", icon_url=avatar,)
        embed.set_image(url=avatar)
        await interaction.response.send_message(embed=embed)

    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None) -> None:
        if member is None:
            member = interaction.user

        user_created_at = member.created_at.strftime("%b %d, %Y %I:%M %p")
        joined_at = member.joined_at.strftime("%b %d, %Y %I:%M %p")

        embed = discord.Embed(color=member.color)
        embed.set_thumbnail(url=member.avatar)
        embed.set_author(name=f"{member.name}'s Info", icon_url=member.avatar)
        embed.add_field(
            name="Tag", value=f"```{member.name}#{member.discriminator}```", inline=False)
        embed.add_field(name="ID", value=f"```{member.id}```", inline=False)
        embed.add_field(name="Creation",
                        value=f"```{user_created_at}```", inline=False)
        embed.add_field(
            name="Avatar", value=f"[Click here]({member.avatar})", inline=False)
        embed.add_field(name="Joined", value=f"{joined_at}", inline=True)
        embed.add_field(name="Nickname", value=f"{member.nick}", inline=True)
        embed.add_field(name="Highest Role",
                        value=f"{member.top_role.mention}", inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=False)

    async def base64decode(self, interaction: discord.Interaction, text: discord.Message) -> None:
        try:
            decoded = base64.b64decode(text.content).decode("utf-8", "ignore")
            await interaction.response.send_message(f"||{decoded}||", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

    async def base64encode(self, interaction: discord.Interaction, message: discord.Message) -> None:
        try:
            text = message.content
            string_bytes = text.encode("ascii")
            base64_bytes = base64.b64encode(string_bytes)
            base64_string = base64_bytes.decode("ascii")
            await interaction.response.send_message(f"||{base64_string}||", ephemeral=False)
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(util_apps(bot))
