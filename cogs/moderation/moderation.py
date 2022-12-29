from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands


class moderationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="resetnickname", description="Reset nickname")
    @app_commands.describe(member="The user whose nickname should be resetted")
    async def resetnickname(
        self, interaction: discord.Interaction, member: discord.Member
    ):
        if interaction.user.guild_permissions.manage_nicknames:
            await member.edit(nick=member.name)
            await interaction.response.send_message(
                f"Cleared the nickname of {member.name}"
            )
        else:
            resetnickembed = discord.Embed(
                title="Error", color=discord.Color.dark_red(), timestamp=datetime.now()
            )

            resetnickembed.add_field(
                name="Something wrent wrong",
                value=f"<@{interaction.user.id}> you don`t have enough permissions to do that.",
            )

            await interaction.response.send_message(
                embed=resetnickembed, ephemeral=True
            )
            resetnickembed.clear_fields()

    @app_commands.command(
        name="clear", description="Deletes a certain number of message"
    )
    @app_commands.describe(amount="The amount of messages to clear")
    async def clear(
        self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]
    ):
        if interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message(
                "Deleted " + str(amount) + " messages", ephemeral=True
            )
            await interaction.channel.purge(limit=amount)
        else:
            clearembed = discord.Embed(
                title="Error", color=discord.Color.dark_red(), timestamp=datetime.now()
            )
            clearembed.add_field(
                name="Something wrent wrong",
                value=f"<@{interaction.user.id}> you don`t have enough permissions to do that.",
            )

            await interaction.response.send_message(embed=clearembed, ephemeral=True)
            clearembed.clear_fields()

    @app_commands.command(name="nickname", description="Changes the bot's nickname")
    @app_commands.describe(nickname="The nickname you want the bot to have")
    async def nickname(self, interaction: discord.Interaction, nickname: str = None):
        if interaction.user.guild_permissions.manage_nicknames:
            if nickname is None:
                nickname = str(self.bot.user.name)

                await interaction.guild.get_member(self.bot.user.id).edit(nick=nickname)
                embed = discord.Embed(title="Nickname changed", color=0x00D9FF)
                embed.add_field(name="Changed by ",
                                value=interaction.user.mention)
                embed.add_field(name="Changed to ", value=nickname)

                await interaction.response.send_message(embed=embed)
            else:
                await interaction.guild.get_member(self.bot.user.id).edit(nick=nickname)
                embed = discord.Embed(title="Nickname changed", color=0x00D9FF)
                embed.add_field(name="Changed by ",
                                value=interaction.user.mention)
                embed.add_field(name="Changed to ", value=nickname)

                await interaction.response.send_message(embed=embed)
        else:
            nickembed = discord.Embed(
                title="Error", color=discord.Color.dark_red(), timestamp=datetime.now()
            )
            nickembed.add_field(
                name="Something wrent wrong",
                value=f"<@{interaction.user.id}> you don`t have enough permissions to do that.",
            )

            await interaction.response.send_message(embed=nickembed, ephemeral=True)
            nickembed.clear_fields()

    @app_commands.command(name="setnickname", description="Changes a user's nickname")
    @app_commands.describe(nickname="The nickname you want a user to have")
    @app_commands.describe(member="The member you want to give the nickname to")
    async def setnickname(
        self, interaction: discord.Interaction, nickname: str, member: discord.Member
    ):
        if interaction.user.guild_permissions.manage_nicknames:
            if member == self.bot.user:
                embed = discord.Embed(
                    title=":x: Command Error", colour=0x992D22
                )  # Dark Red
                embed.add_field(
                    name="Error", value="Please use /nickname to change my nickname"
                )
                embed.timestamp = datetime.now()
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return False

            if member is None:
                member = interaction.user

            await member.edit(nick=nickname)
            if nickname:
                embed = discord.Embed(title="Nickname changed", color=0x00D9FF)
                embed.add_field(name="Changed by ",
                                value=interaction.user.mention)
                embed.add_field(name="Changed to ", value=nickname)
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(title="Nickname changed", color=0x00D9FF)
                embed.add_field(name="Changed by ",
                                value=interaction.user.mention)
                embed.add_field(name="Changed to ", value=nickname)
                await interaction.response.send_message(embed=embed)
        else:
            nickembed = discord.Embed(
                title="Error", color=discord.Color.dark_red(), timestamp=datetime.now()
            )
            nickembed.add_field(
                name="Something wrent wrong",
                value=f"<@{interaction.user.id}> you don`t have enough permissions to do that.",
            )

            await interaction.response.send_message(embed=nickembed, ephemeral=True)
            nickembed.clear_fields()

    @app_commands.command(name="poll", description="Creates a simple poll")
    @app_commands.describe(text="Your yes/no question")
    async def poll(self, interaction: discord.Interaction, text: str):
        if interaction.user.guild_permissions.view_audit_log:
            channel = interaction.channel
            channel = discord.utils.get(
                interaction.guild.channels, name=channel.name)
            await interaction.response.send_message("Okay", ephemeral=True)
            embed = discord.Embed(title=text, color=0x00D9FF)
            message = await channel.send(embed=embed)
            await message.add_reaction("✅")
            await message.add_reaction("❌")
        else:
            poolembed = discord.Embed(
                title="Error", color=discord.Color.dark_red(), timestamp=datetime.now()
            )
            poolembed.add_field(
                name="Something wrent wrong",
                value=f"<@{interaction.user.id}> you don`t have enough permissions to do that.",
            )

            await interaction.response.send_message(embed=poolembed, ephemeral=True)
            poolembed.clear_fields()

    @app_commands.command(name="say", description="Let the bot say something (Use '\\\\' as linebrake)")
    @app_commands.describe(message="The text you want the bot to say")
    async def say(self, interaction: discord.Interaction, message: str, channel: discord.TextChannel = None):
        if "\\" in message:
            message = message.replace("\\", "\n")

        if not interaction.user.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="Error",
                description=f"<@{interaction.user.id}> you don`t have enough permissions to do that.",
                color=discord.Color.dark_red(),
                timestamp=datetime.now(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if channel is None:
            channel = interaction.channel
        await channel.send(message)
        await interaction.response.send_message(f"Sent message to {channel.mention}", ephemeral=True)



async def setup(bot):
    await bot.add_cog(moderationCog(bot))
