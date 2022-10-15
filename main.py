import discord, os, smtplib
from discord import app_commands
from dotenv import load_dotenv
load_dotenv()

email_address = os.getenv('EMAIL')
email_password = os.getenv('PASSWORD')
smtp_server = os.getenv('SMTP')
smtp_port = os.getenv('SMTP_PORT')
bot_token = os.getenv('TOKEN')
medusa_url = os.getenv('MEDUSA_URL')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

bot.run(bot_token)