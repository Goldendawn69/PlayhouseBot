import discord
from discord.ext import commands
from Configuration import Configuration, load_config


class MonitorLinks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.cfg = load_config('config.json')

    @commands.Cog.listener()
    async def on_message(self, message):

        checklist = ['http://', 'https://']

        if message.author.bot or not message.guild:
            return
        if message.channel.id not in self.cfg.monitored_channels:
            return

        if message.attachments:
            await self.managed_attached_files(message)
        else:
            if any(checklist in message.content for checklist in checklist):
                await self.manage_link_message(message)

    async def delete_message(self, message):
        await message.delete()
        return

    async def manage_link_message(self, message):

        log_channel = await self.get_msglog_channel(message.guild)
        sfw_media_channel = await self.bot.fetch_channel(self.cfg.chan_sfw_media)
        nsfw_media_channel = await self.bot.fetch_channel(self.cfg.chan_nsfw_media)
        helpdesk_channel = await self.bot.fetch_channel(self.cfg.chan_helpdesk)
        author = message.author

        if message.content.startswith('https://tenor.com/view/'):
            return
        else:
            await log_channel.send(f'<@{author.id}> posted a message in <#{message.channel.id}> which included link(s).\n\nMessage Details: {message}\n\n"{message.content}".\n\nA DM was sent to the author, and the message was deleted.')

            await author.send(f'Dear {author},\n\nThe message you just posted in <#{message.channel.id}> is not allowed due to it having included link(s).\n\n{message.content}\n\nAs links are not allowed in the channel, if you wish to share your content, please post to <#{sfw_media_channel.id}> or if NSFW content to <#{nsfw_media_channel.id}>, else you can use the Discord inbuilt GIF functionality.\n\nAny questions to this can be posted in the <#{helpdesk_channel.id}> or please reply to this DM, and quote the message id: #{message.id}')

            await self.delete_message(message)
        return

    async def get_msglog_channel(self, guild: discord.Guild):
        channel_id = self.cfg.servers[guild.id].chan_message_log
        channel = await self.bot.fetch_channel(channel_id)
        return channel

    async def managed_attached_files(self, message):

        log_channel = await self.get_msglog_channel(message.guild)
        sfw_media_channel = await self.bot.fetch_channel(self.cfg.chan_sfw_media)
        nsfw_media_channel = await self.bot.fetch_channel(self.cfg.chan_nsfw_media)
        helpdesk_channel = await self.bot.fetch_channel(self.cfg.chan_helpdesk)
        message_id = message.id
        author = message.author
        await log_channel.send(f'<@{author.id}> posted a message in <#{message.channel.id}> which included attachment(s).\n\nMessage Details: {message}.\n\n{message.content}\n{message.attachments[0].url}\n\nA DM was sent to the author, and the message was deleted.')
        await author.send(f'Dear {author},\n\nThe message you just posted in <#{message.channel.id}> is not allowed due to it having an attached image.\n\n{message.content}\n{message.attachments[0].url}\n\nAs attachements are not allowed in the channel, if you wish to share your content, please post to <#{sfw_media_channel.id}> or if NSFW content to <#{nsfw_media_channel.id}>, else you can use the Discord inbuilt GIF functionality.\n\nAny questions to this can be posted in the <#{helpdesk_channel.id}> or please reply to this DM, and quote the message id: #{message.id}')
        await self.delete_message(message)
        return


def setup(bot):
    bot.add_cog(MonitorLinks(bot))
