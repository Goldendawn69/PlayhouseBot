import discord
from discord.ext import commands
from discord.ext.commands import CheckFailure, check


class GeneralCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='areyouonline')
    async def areyouonline(self, ctx):
        # Get male and female roles
        male = discord.utils.find(lambda r: r.name == 'Male', ctx.guild.roles)
        female = discord.utils.find(
            lambda r: r.name == 'Female', ctx.guild.roles)

        # reply according to role
        if male in ctx.author.roles:
            await ctx.send("I am not telling you")
        elif female in ctx.author.roles:
            await ctx.send("Yea gurl.")
        else:
            await ctx.send("Yea.")

    @commands.command(name='say')
    @commands.has_permissions(administrator=True, manage_messages=True, manage_roles=True)
    async def say(self, ctx, channel: discord.TextChannel, *, message):
        await channel.send(message, files=ctx.message.attachments)


def setup(bot):
    bot.add_cog(GeneralCommands(bot))
