import discord
from discord.ext import commands
from Configuration import Configuration, load_config
from library.DiscordFunctions import get_user_from_mention
from library.DiscordReactions import add_confirmation_reaction


class Ban(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.cfg = load_config('config.json')

    @commands.command(name='ban')
    @commands.has_permissions(administrator=True, ban_members=True)
    async def ban(self, ctx, mention: discord.User = None, *, reason='[no reason given]'):
        if not mention:
            await ctx.send("Who would you like me to ban, {0:mention}?".format(ctx.message.author))
            pass

        user = mention

        await user.send(f"You have been banned in {ctx.guild.name} for the following reason:\n{reason}")
        await user.send(f"If you wish to discuss your banning please reply to this message.")

        await ctx.guild.ban(user, reason=reason)

        member_log = await self.bot.fetch_channel(self.cfg.servers[ctx.guild.id].chan_member_log)
        await member_log.send(f"{user.name}(id: {user.id}) was banned for '{reason}'")

        await add_confirmation_reaction(self, ctx.guild.id, ctx.message)

    @commands.command(name='unban')
    @commands.has_permissions(administrator=True, ban_members=True)
    async def unban(self, ctx, *, mention=None, reason='[No Reason given]'):

        if not mention:
            await ctx.send("Who would you like me to unban")
            return

        banned_users = await ctx.guild.bans()
        mentionid = await get_user_from_mention(mention)

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.id) == (mentionid):
                await ctx.guild.unban(user)
                member_log = await self.bot.fetch_channel(self.cfg.servers[ctx.guild.id].chan_member_log)
                await member_log.send(f"{user.id}) was unbanned by [tbc], reason: {reason}")
                await add_confirmation_reaction(self, ctx.guild.id, ctx.message)
                return

        user = discord.utils.find(lambda m: mentionid, banned_users)

        if not user:
            return

        await ctx.guild.unban(user)
        member_log = await self.bot.fetch_channel(self.cfg.servers[ctx.guild.id].chan_member_log)
        await member_log.send(f"{user.id}) was unbanned")

        await add_confirmation_reaction(self, ctx.guild.id, ctx.message)


def setup(bot):
    bot.add_cog(Ban(bot))
