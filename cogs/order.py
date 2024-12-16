import discord
from discord import app_commands
from discord.ext import commands
import requests
import datetime
from dotenv import load_dotenv
import os

load_dotenv()
medusa_url = os.getenv("MEDUSA_URL")


class OrderCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="order", description="Check a particular order information"
    )
    async def order(self, interaction: discord.Interaction, order_id: str):
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
            order = res["order"]
            first_name = order["shipping_address"]["first_name"]
            last_name = order["shipping_address"]["last_name"]
            phone = order["shipping_address"]["phone"]
            address = (
                (
                    order["shipping_address"]["address_1"]
                    + ", "
                    + order["shipping_address"]["city"]
                    + ", "
                    + order["shipping_address"]["province"]
                    + ", "
                    + order["shipping_address"]["postal_code"]
                )
                + ", "
                + order["shipping_address"]["country_code"].upper()
            )
            email = order["customer"]["email"]

            embed = discord.Embed(
                title="Order information",
                description=f"Order ID: `{order_id}`",
                color=0x2ECC71,
                timestamp=datetime.datetime.utcnow(),
            )
            embed.add_field(
                name="Customer Details",
                value=f"• :bust_in_silhouette: Name: `{first_name} {last_name}`\n• :mobile_phone: Phone: `{phone}`\n• :e_mail: Email: `{email}`",
                inline=False,
            )
            embed.add_field(
                name="Shipping Address",
                value=f"• :hotel: Address: `{address}`",
                inline=False,
            )
            embed.set_thumbnail(url="https://i.imgur.com/yFkhOEx.jpg")
            embed.set_footer(text=f"Requested by {user}", icon_url=avatar_url)
            await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(OrderCog(bot))
