import discord
import logging

from discord.ext import commands
from dotenv import load_dotenv
from os import environ

load_dotenv()
bot_token = environ['DISCORD_TOKEN']

bot = discord.ext.commands.Bot(command_prefix=('!bb ', '!bb'))

log = logging.getLogger('bot_log')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(name)s: %(levelname)s %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler('bot.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

if len(log.handlers) > 0:
    log.handlers = []

log.addHandler(stream_handler)
log.addHandler(file_handler)

@bot.event
async def on_ready():
    log.debug('Connected to discord')

@bot.command(name='rules_confirmed')
async def new_user_confirmed_rules(ctx):
    """
    If user sends the rules_confirmed command to the rules channel
    and does not have the Ice Beams role, user has Ice Beams added to their roles.
    Otherwise, a dm is sent to the user explaining that they already have Ice Beams roles
    and that the command will do nothing further.
    Afterwards, the user input bot command is deleted from the channel to keep the rules channel clean.
    """
    # log.debug('rules_confirmed command received')
    # log.debug(f'ctx_channel: {ctx.channel.name}, ctx_author.roles: {ctx.author.roles}')
    # log.debug(f'role names: {[role.name for role in ctx.author.roles]}')
    # log.debug(f'first condition: {ctx.channel.name == "rules"}')
    # log.debug(f'second condition: {"Ice Beams" not in [role.name for role in ctx.author.roles]}')
    if ctx.channel.name == 'rules' and 'Ice Beams' not in [role.name for role in ctx.author.roles]:
        ice_beam_role = discord.utils.get(ctx.guild.roles, name='Ice Beams')
        await ctx.author.add_roles(ice_beam_role, reason='User verified rules')
        log.debug(f'Ice Beams role added to user: {ctx.author.display_name}')
    else:
        log.debug(f'User {ctx.author.display_name} is already a member of Ice Beams')
        await ctx.author.create_dm()
        await ctx.author.dm_channel.send(
            f'Hi {ctx.author.display_name}! '
            'Command rules_confirmed is meant to add new users to Ice Beams once they have acknowledged BoltBeam\'s rules. '
            'Since you already have the Ice Beams role, no action will be taken now. '
            'Note: I am a bot user BEEP BOOP'
        )

    # delete bot command
    await ctx.message.delete()


bot.run(bot_token)
