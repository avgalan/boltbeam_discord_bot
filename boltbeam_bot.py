import logging

from discord.ext import commands
from os import environ

load_dotenv()
bot_token = environ['DISCORD_TOKEN']

bot = commands.Bot(command_prefix='!')

log = logging.getLogger('bot_log')
log.setLevel(20)
formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(name)s: %(levelname)s %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(20)
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler('bot.log')
file_handler.setLevel(20)
file_handler.setFormatter(formatter)

if len(log.handlers) > 0:
    log.handlers = []

log.addHandler(stream_handler)
log.addHandler(file_handler)

@bot.event
async def on_ready():
    pass

@bot.command(name='rules_confirmed')
async def new_user_confirmed_rules(ctx):
    if ctx.channel == 'rules':
        # change user group
        await ctx.author.add_roles('new role name here', reason='User verified rules')
        # delete bot command
        await ctx.message.delete()

bot.run(bot_token)
