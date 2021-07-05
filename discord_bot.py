# bot.py
import os
from logger import ActivityLogger
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
child_connection = None
client = discord.Client()
logger = ActivityLogger(__name__)


@client.event
async def on_ready():
    logger.log_event_info(f'{client.user} has connected to Discord!')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_contents = message.content
    if message_contents.startswith('att '):
        message_contents = message_contents.lstrip('att ')
        space = message_contents.index(' ')
        attendance_token, attendance_message = message_contents[:space], message_contents[space + 1:]
        client.child_conn.send(attendance_message)
        logger.log_event_info('Attendance Token {} recorded'.format(attendance_token))
        await message.channel.send('OK')


def run_discord_bot(child_conn):
    client.child_conn = child_conn
    client.run(TOKEN)
