import base64
import json
from datetime import datetime

import discord
import requests
from discord import app_commands
from discord.ext import commands


class appsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commands = [
            ("Get Message ID", self.get_message_id),
            ("Nuke Channel", self.nuke_channel),
            ("Get avatar", self.getavatar),
            ("User Info", self.userinfo),
            ("Encode base64", self.base64encode),
            ("Decode base64", self.base64decode)
        ]
        self.create_context_menus()

    def create_context_menus(self):
        for name, callback in self.commands:
            menu = app_commands.ContextMenu(name=name, callback=callback)
            self.bot.tree.add_command(menu)



    async def get_message_id(self, interaction: discord.Interaction, message: discord.Message) -> None:
        await interaction.response.send_message(message.id, ephemeral=True)

    async def getavatar(self, interaction: discord.Interaction, member: discord.Member = None) -> None:
            if member is None:
                member = interaction.user
            avatar = member.avatar
            embed = discord.Embed(title=f"{member.name}'s Avatar", url=avatar, color=0x00EFDB,)
            embed.set_author(name=f"{member.name}'s avatar", url=f"https://discord.com/users/{member.id}", icon_url=avatar,)
            embed.set_image(url=avatar)
            await interaction.response.send_message(embed=embed)

    async def userinfo(self, interaction: discord.Interaction, user: discord.Member = None) -> None:
        if user is None:
            user = interaction.user

        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(title=f"{user.name}'s Info", color=0x00CCFF)
        embed.set_author(name=str(user), icon_url=user.avatar)
        embed.set_thumbnail(url=user.avatar)
        embed.add_field(name="Name", value=user.name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Join position", value=str(sorted(interaction.guild.members, key=lambda m: m.joined_at).index(user) + 1))
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format), inline=True)
        embed.add_field(name="Account created", value=user.created_at.strftime(date_format), inline=True)
        embed.add_field(name="🤖 Bot", value=user.bot, inline=True)
        embed.add_field(name="Nickname", value=user.nick, inline=True)
        embed.add_field(name="Highest role", value=user.top_role.mention, inline=True)
        embed.add_field(name="Roles", value=", ".join([r.mention for r in user.roles]), inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def nuke_channel(self, interaction: discord.Interaction, message: discord.Message) -> None:
        if interaction.user.guild_permissions.manage_channels:
            nuke_channel = discord.utils.get(interaction.guild.channels, name=interaction.channel.name)

            if nuke_channel is not None:
                new = await nuke_channel.clone(reason="Has been Nuked!")
                await nuke_channel.delete()
                await new.send("THIS CHANNEL HAS BEEN NUKED!")
            else:
                await interaction.response.send_message(f"No channel named {interaction.channel.name} was found!", ephemeral=True)
        else:
            await interaction.response.send_message(f"{interaction.user.mention} you don't have enough permissions to do that.",ephemeral=True)


    async def base64decode(self, interaction: discord.Interaction, message: discord.Message) -> None:
        try:
            text = message.content
            decoded = base64.b64decode(text).decode("utf-8", "ignore")
            await interaction.response.send_message(f"Your decoded text:\n || {str(decoded)} ||", ephemeral=False)
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

    async def base64encode(self, interaction: discord.Interaction, message: discord.Message) -> None:
        try:
            text = message.content
            string_bytes = text.encode("ascii")

            base64_bytes = base64.b64encode(string_bytes)
            base64_string = base64_bytes.decode("ascii")
            await interaction.response.send_message(f"Your encoded text:\n || {str(base64_string)} ||", ephemeral=False)
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(appsCog(bot))
