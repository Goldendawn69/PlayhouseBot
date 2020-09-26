import json
from ServerCfg import ServerCfg

class Configuration:
	def __init__(self, token = '', prefix = '.', description = '', name = '', bot_user_id = '', chan_forward_dm = '', guild_remind = '', role_remind = '', chan_remind = '', chan_sfw_media = '', chan_nsfw_media = '', chan_helpdesk = '', monitored_channels = '', servers = {}):
		self.token = token
		self.prefix = prefix
		self.description = description
		self.name = name
		self.bot_user_id = bot_user_id
		self.chan_forward_dm = chan_forward_dm
		self.guild_remind = guild_remind
		self.role_remind = role_remind
		self.chan_remind = chan_remind
		self.chan_sfw_media = chan_sfw_media
		self.chan_nsfw_media = chan_nsfw_media
		self.chan_helpdesk = chan_helpdesk
		self.monitored_channels = monitored_channels
		self.servers = {}
		for key, value in servers.items():
			fields = ['cate_personal_vc', 'chan_personal_vc', 'chan_message_log', 'chan_member_log', 'confirm_sent_reaction', 'negative_reaction', 'reminder_user_id', 'reminder_bump_minutes']
			args = [value[field] for field in fields]
			srv = ServerCfg(*args)
			self.servers[int(key)] = srv

def load_config(filename):
	with open(filename) as cfg_file:
		jsonfile = json.loads(cfg_file.read())

	args = (
		jsonfile['token'],
		jsonfile['prefix'],
		jsonfile['description'],
		jsonfile['name'],
		jsonfile['bot_user_id'],
		jsonfile['chan_forward_dm'],
		jsonfile['guild_remind'],
		jsonfile['role_remind'],
		jsonfile['chan_remind'],
		jsonfile['chan_sfw_media'],
		jsonfile['chan_nsfw_media'],
		jsonfile['chan_helpdesk'],
		jsonfile['monitored_channels'],
		jsonfile['servers']
	)

	conf = Configuration(*args)
	return conf
