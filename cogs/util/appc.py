import base64
import sys
from helpers.utilFunctions import checkMember
import discord
from discord import app_commands
from discord.ext import commands

sys.dont_write_bytecode = True

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
        checkedMember = checkedMember(interaction=interaction, member=member)
        avatar = checkedMember.avatar
        embed = discord.Embed(
            title=f"Download {checkedMember.display_name}'s Avatar",
            url=avatar,
            color=0x00EFDB
        ).set_author(
            name=f"{checkedMember.display_name}'s avatar",
            url=f"https://discord.com/users/{checkedMember.id}", icon_url=avatar
        ).set_image(
            url=avatar
        )
        await interaction.response.send_message(embed=embed)

    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None) -> None:
        checkedMember = checkedMember(interaction=interaction, member=member)

        user_created_at = checkedMember.created_at.strftime("%b %d, %Y %I:%M %p")
        joined_at = ""  # Initialize the variable here to avoid NameError
        nickname = ""  # Initialize nickname variable
        top_role = ""  # Initialize top_role variable

        if interaction.guild:
            joined_at = checkedMember.joined_at.strftime("%b %d, %Y %I:%M %p")
            nickname = checkedMember.nick if checkedMember.nick else "None"  # Set nickname or 'None' if no nickname
            top_role = checkedMember.top_role.mention  # Mention the highest role

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
        ).add_field(
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
            name="Avatar",
            value=f"[Click here]({checkedMember.avatar})",
            inline=False
        )

        if interaction.guild:  # Add server-specific fields only if the command is used in a guild
            embed.add_field(
                name="Joined",
                value=f"{joined_at}",
                inline=True
            ).add_field(
                name="Nickname",
                value=f"{nickname}",
                inline=True
            ).add_field(
                name="Highest Role",
                value=f"{top_role}",
                inline=True
            )

        await interaction.response.send_message(embed=embed)


    async def base64decode(self, interaction: discord.Interaction, text: discord.Message) -> None:
        try:
            decoded = base64.b64decode(text.content).decode("utf-8", "ignore")
            await interaction.response.send_message(content=f"||{decoded}||", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(content=f"Error: {e}", ephemeral=True)

    async def base64encode(self, interaction: discord.Interaction, message: discord.Message) -> None:
        try:
            text = message.content
            string_bytes = text.encode("ascii")
            base64_bytes = base64.b64encode(string_bytes)
            base64_string = base64_bytes.decode("ascii")
            await interaction.response.send_message(content=f"||{base64_string}||", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(content=f"Error: {e}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(util_apps(bot))
