from datetime import datetime
import json
import discord
from discord import app_commands
from discord.ext import commands
import requests
import base64

with open("config.json", "r", encoding="UTF-8") as configfile:
    config = json.load(configfile)
    apikey = config["apikey"]
configfile.close()


class appsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.get_messageid_menu = app_commands.ContextMenu(name="Get Message ID", callback=self.get_message_id,)
        self.bot.tree.add_command(self.get_messageid_menu)
        self.nukechannel_menu = app_commands.ContextMenu(name="Nuke Channel", callback=self.nuke_channel,)
        self.bot.tree.add_command(self.nukechannel_menu)
        self.getavatar_menu = app_commands.ContextMenu(name="Get avatar",callback=self.getavatar,)
        self.bot.tree.add_command(self.getavatar_menu)
        self.userinfo_menu = app_commands.ContextMenu(name="User Info",callback=self.userinfo,)
        self.bot.tree.add_command(self.userinfo_menu)
        self.get_mock_menu = app_commands.ContextMenu(name="Mock text in message",callback=self.mock,)
        self.bot.tree.add_command(self.get_mock_menu)
        self.get_base64encode_menu = app_commands.ContextMenu(name="Encode base64",callback=self.base64encode,)
        self.bot.tree.add_command(self.get_base64encode_menu)
        self.get_base64decode_menu = app_commands.ContextMenu(name="Decode base64",callback=self.base64decode,)
        self.bot.tree.add_command(self.get_base64decode_menu)


    async def get_message_id(self, interaction: discord.Interaction, message: discord.Message) -> None:
        await interaction.response.send_message(message.id, ephemeral=True)

    async def mock(self, interaction: discord.Interaction, message: discord.Message):
        try:
            content = message.content
            getinformation = requests.get(url=f"https://anditv.it/api/?api_key={apikey}&function=mock&text={content}")
            if getinformation.status_code != 200:
                errorres = discord.Embed(
                    title='API Error',
                    color=discord.Color.dark_red()
                ).clear_fields(
                ).add_field(
                    name='Something wrent wrong',
                    value='Connection to api failed'
                ).set_footer(
                    text=interaction.user.name,
                    icon_url=interaction.user.avatar,
                )
                return await interaction.response.send_message(embed=errorres, ephemeral=True)

            result = getinformation.json()['text']
            await interaction.response.send_message(result, ephemeral=True)
        except Exception as e:
            print(e)

    async def getavatar(
        self, interaction: discord.Interaction, member: discord.Member) -> None:
        if member is None:
            member = interaction.user
        embed = discord.Embed(
            title="Download Avatar",
            url=member.avatar,
            color=0x00EFDB,
        )
        embed.set_author(
            name=member.name + "`s avatar",
            url="https://discord.com/users/" + str(member.id),
            icon_url=member.avatar,
        )
        embed.set_image(url=member.avatar)
        await interaction.response.send_message(embed=embed)

    async def userinfo(
        self, interaction: discord.Interaction, user: discord.Member) -> None:

        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(title=f"{user.name}'s Info", color=0x00CCFF)
        embed.set_author(name=str(user), icon_url=user.avatar)
        embed.set_thumbnail(url=user.avatar)
        embed.add_field(name="Name", value=user.name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(
            name="Joined", value=user.joined_at.strftime(date_format), inline=True
        )
        members = sorted(interaction.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position",
                        value=str(members.index(user) + 1))
        embed.add_field(
            name="Account created",
            value=user.created_at.strftime(date_format),
            inline=True,
        )
        embed.add_field(name="🤖 Bot", value=user.bot, inline=True)
        embed.add_field(name="Nickname", value=user.nick, inline=True)
        #         embed.add_field(name='Status', value=user.raw_status, inline=True)

        embed.add_field(name="Highest role",
                        value=user.top_role.mention, inline=True)
        rolelist = [r.mention for r in user.roles]
        roles = ", ".join(rolelist)
        embed.add_field(name="Roles", value=roles, inline=True)
        embed.set_thumbnail(url=user.avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def nuke_channel(
        self, interaction: discord.Interaction, message: discord.Message) -> None:
        if interaction.user.guild_permissions.manage_channels:
            if channel is None:
                channel = interaction.channel
            nuke_channel = discord.utils.get(
                interaction.guild.channels, name=channel.name
            )

            if nuke_channel is not None:
                new_channel = await nuke_channel.clone(reason="Has been Nuked!")
                await nuke_channel.delete()
                await new_channel.send("THIS CHANNEL HAS BEEN NUKED!")

            else:
                await interaction.response.send_message(
                    f"No channel named {channel.name} was found!", ephemeral=True
                )
        else:
            nukeembed = discord.Embed(
                title="Error", color=discord.Color.dark_red(), timestamp=datetime.now()
            )

            nukeembed.add_field(
                name="Something wrent wrong",
                value=f"<@{interaction.user.id}> you don`t have enough permissions to do that.",
            )

            await interaction.response.send_message(embed=nukeembed, ephemeral=True)
            nukeembed.clear_fields()



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
