import discord
from discord.ext import commands

def checkMember(interaction: discord.Interaction, member: discord.Member = None) -> discord.Member:
    if member == None:
        return interaction.author
    return member