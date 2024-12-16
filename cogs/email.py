import discord
from discord import app_commands
from discord.ext import commands
import smtplib
from email.message import EmailMessage
import requests
import datetime
from dotenv import load_dotenv
import os

load_dotenv()
smtp_server = os.getenv("SMTP")
smtp_port = os.getenv("SMTP_PORT")
email_address = os.getenv("EMAIL")
email_password = os.getenv("PASSWORD")
medusa_url = os.getenv("MEDUSA_URL")


class EmailCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="email", description="Send an email to the customer")
    async def email(
        self,
        interaction: discord.Interaction,
        order_id: str,
        *,
        email_subject: str,
        email_body: str,
    ):
        user = interaction.user
        avatar_url = user.avatar
        r = requests.get(medusa_url + "/store/orders/" + order_id)

        if r.status_code == 404:
            embed = discord.Embed(
                title="Order not found :x:",
                description=f"The order you are looking for with the ID `{order_id}` does not exist",
                color=0xE74C3C,
                timestamp=datetime.datetime.utcnow(),
            )
            embed.set_thumbnail(url="https://i.imgur.com/yFkhOEx.jpg")
            embed.set_footer(text=f"Requested by {user}", icon_url=avatar_url)
            await interaction.response.send_message(embed=embed)
        elif r.status_code == 200:
            res = r.json()
            customer_email = res["order"]["customer"]["email"]

            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(email_address, email_password)
                message = f"Subject: {email_subject}\n\n{email_body}"
                server.sendmail(email_address, customer_email, message)
                server.quit()

                embed = discord.Embed(
                    title="Email sent :white_check_mark:",
                    description=f"An email has been sent to `{customer_email}`!",
                    color=0x2ECC71,
                    timestamp=datetime.datetime.utcnow(),
                )
                embed.set_thumbnail(url="https://i.imgur.com/yFkhOEx.jpg")
                embed.set_footer(text=f"Requested by {user}", icon_url=avatar_url)
                await interaction.response.send_message(embed=embed)
            except Exception as e:
                print(e)
                embed = discord.Embed(
                    title="Error :x:",
                    description="An error occurred while trying to send the email",
                    color=0xE74C3C,
                    timestamp=datetime.datetime.utcnow(),
                )
                embed.set_thumbnail(url="https://i.imgur.com/yFkhOEx.jpg")
                embed.set_footer(text=f"Requested by {user}", icon_url=avatar_url)
                await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="coolemail", description="Send a cool email to the customer"
    )
    async def coolemail(
        self,
        interaction: discord.Interaction,
        order_id: str,
        email_subject: str,
        email_headline: str,
        email_body: str,
    ):
        user = interaction.user
        avatar_url = user.avatar
        r = requests.get(medusa_url + "/store/orders/" + order_id)

        if r.status_code == 404:
            embed = discord.Embed(
                title="Order not found :x:",
                description=f"The order you are looking for with the ID `{order_id}` does not exist",
                color=0xE74C3C,
                timestamp=datetime.datetime.utcnow(),
            )
            embed.set_thumbnail(url="https://i.imgur.com/yFkhOEx.jpg")
            embed.set_footer(text=f"Requested by {user}", icon_url=avatar_url)
            await interaction.response.send_message(embed=embed)
            return
        elif r.status_code == 200:
            res = r.json()
            customer_email = res["order"]["customer"]["email"]
            customer_first_name = res["order"]["customer"]["first_name"]
            embed = discord.Embed(
                title="Cool email sent :white_check_mark:",
                description=f"An email has been sent to `{customer_email}`!",
                color=0x2ECC71,
                timestamp=datetime.datetime.utcnow(),
            )
            embed.set_thumbnail(url="https://i.imgur.com/yFkhOEx.jpg")
            embed.set_footer(text=f"Requested by {user}", icon_url=avatar_url)

            msg = EmailMessage()
            msg["Subject"] = email_subject
            msg["From"] = email_address
            msg["To"] = customer_email
            msg.set_content("Test Message")
            html_message = open("template.html").read()
            html_message = (
                html_message.replace("{first_name}", customer_first_name)
                .replace("{email_headline}", email_headline)
                .replace("{email_body}", email_body)
            )
            msg.add_alternative(html_message, subtype="html")

            try:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(email_address, email_password)
                    server.send_message(msg)
                    await interaction.response.send_message(embed=embed)
            except Exception as e:
                print(e)
                embed = discord.Embed(
                    title="Error :x:",
                    description="An error occurred while trying to send the email",
                    color=0xE74C3C,
                    timestamp=datetime.datetime.utcnow(),
                )
                embed.set_thumbnail(url="https://i.imgur.com/yFkhOEx.jpg")
                embed.set_footer(text=f"Requested by {user}", icon_url=avatar_url)
                await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(EmailCog(bot))
