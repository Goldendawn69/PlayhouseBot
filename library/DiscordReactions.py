import discord
from discord.ext import commands
from Configuration import Configuration, load_config
from discord.ext.commands import CheckFailure, check


async def add_confirmation_reaction(self, guildid, message):
    """Adds a reaction a positive confirmation reaction to a message

    Args:
        guildid ([int]): Id of the Server where the reaction is required
        message ([object]): Message that the reaction is required to be added to
    """
    reactionId = self.cfg.servers[guildid].confirm_sent_reaction
    reactionIcon = '\N{WHITE HEAVY CHECK MARK}'
    await message.add_reaction(reactionIcon)


async def add_negative_reaction(guildid, message):
    """Adds a reaction a positive confirmation reaction to a message

    Args:
        guildid ([int]): Id of the Server where the reaction is required
        message ([object]): Message that the reaction is required to be added to
    """
    #reactionId = self.cfg.servers[guild.id].confirm_sent_reaction
    reactionIcon = '\N{CROSS MARK}'
    await message.add_reaction(reactionIcon)
