import sys
import discord
from discord import app_commands
from discord.ext import commands

sys.dont_write_bytecode = True

class mod_apps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commands = [
            ("Nuke Channel", self.nuke_channel)
        ]
        self.create_context_menus()

    def create_context_menus(self):
        # Loop over the list of commands and create a context menu for each one
        for name, callback in self.commands:
            menu = app_commands.ContextMenu(name=name, callback=callback)
            # Add the context menu to the application command tree
            self.bot.tree.add_command(menu)

    async def nuke_channel(self, interaction: discord.Interaction, message: discord.Message) -> None:
        # Check if the interaction is in a guild (server) context
        if interaction.guild is None:
            embed = discord.Embed(
                title="Command Not Available",
                description="This command cannot be used in direct messages (DMs). Please use it in a server context.",
                color=discord.Color.red()
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        # Check if the bot has permission to manage channels
        if not interaction.guild.me.guild_permissions.manage_channels:
            embed = discord.Embed(
                title="Bot Permissions Error",
                description="I don't have enough permissions to manage channels.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar)
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        # Check if the user has permission to manage channels
        if not interaction.user.guild_permissions.manage_channels:
            embed = discord.Embed(
                title="Permissions Error",
                description=f"{interaction.user.mention}, you don't have enough permissions to use this command.",
                color=discord.Color.red()
            ).set_footer(
                text=f"Requested by {interaction.user.name}",
                icon_url=interaction.user.avatar
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        channel = discord.utils.get(interaction.guild.channels, name=interaction.channel.name)
        try:
            await interaction.response.send_message("Channel will be nuked shortly.", ephemeral=True)

            # Clone the channel and move it to the original channel's position, then delete the original channel
            new = await channel.clone(reason="Has been Nuked!")
            await new.edit(position=channel.position)
            await channel.delete()

            # Send an embed in the new channel to indicate that the nuke was successful
            embed = discord.Embed(
                title="Nuke Successful",
                description=f"This channel has been nuked!",
                color=discord.Color.red()
            ).set_image(
                url="https://media.discordapp.net/attachments/811143476522909718/819507596302090261/boom.gif"
            ).set_footer(
                text=f"Requested by {interaction.user.name}",
                icon_url=interaction.user.avatar
            )
            await new.send(embed=embed)
        except discord.HTTPException:
            embed = discord.Embed(
                title="Error",
                description=f"An error occurred while nuking the channel. Please try again later.",
                color=discord.Color.red()
            ).set_footer(
                text=f"Requested by {interaction.user.name}",
                icon_url=interaction.user.avatar
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(mod_apps(bot))
