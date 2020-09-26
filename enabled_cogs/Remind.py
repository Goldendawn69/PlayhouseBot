import discord
from datetime import datetime, timedelta
from discord.ext import tasks, commands
from Configuration import Configuration, load_config
import asyncio


class Remind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = load_config('config.json')
        self.remind_bump.start()

    def cog_unload(self):
        self.remind_bump.cancel()

    @tasks.loop(minutes=5)
    async def remind_bump(self):
        await asyncio.sleep(10)
        chan = await self.bot.fetch_channel(self.cfg.chan_remind)
        guild = await self.bot.fetch_guild(self.cfg.guild_remind)
        bot_id = self.cfg.bot_user_id
        user_id = self.cfg.servers[guild.id].reminder_user_id
        role = guild.get_role(self.cfg.role_remind)
        minutes_between_bumps = self.cfg.servers[guild.id].reminder_bump_minutes

        last_message = await chan.history(limit=1).flatten()
        if (last_message[0].author.id == bot_id):
            return

        latest_message = await chan.history().get(author__id=user_id)

        if (not latest_message):
            return

        rebump_time = latest_message.created_at + \
            timedelta(minutes=minutes_between_bumps)

        if (datetime.utcnow() > rebump_time):
            await chan.send(f'{role.mention} Time to bump!\n!d bump')


def setup(bot):
    bot.add_cog(Remind(bot))
