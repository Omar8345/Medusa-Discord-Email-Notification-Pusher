import discord, os, smtplib, requests, datetime
from discord.ext import commands
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

email_address = os.getenv('EMAIL')
email_password = os.getenv('PASSWORD')
smtp_server = os.getenv('SMTP')
smtp_port = os.getenv('SMTP_PORT')
bot_token = os.getenv('TOKEN')
medusa_url = os.getenv('MEDUSA_URL')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

# On ready
@bot.event
async def on_ready():
    print('Bot is ready - Logged in as {0.user}'.format(bot))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# On command (/order)
@bot.tree.command(name='order', description='Check a particular order information')
async def order(interaction: discord.Interaction, order_id: str):
    user = interaction.user
    avatar_url = user.avatar
    r = requests.get(medusa_url + '/store/orders/' + order_id)
    if r.status_code == 404:
        embed = discord.Embed(
            title='Order not found :x:',
            description=f'The order you are looking for with the ID `{order_id}` does not exist',
            color=0xe74c3c,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url='https://i.imgur.com/yFkhOEx.jpg')
        embed.set_footer(text=f'Requseted by {user}', icon_url=avatar_url)
        await interaction.response.send_message(embed=embed)
    elif r.status_code == 200:
        res = r.json()    
        order = res['order']
        first_name = order['shipping_address']['first_name']
        last_name = order['shipping_address']['last_name']
        phone = order['shipping_address']['phone']
        address = (order['shipping_address']['address_1'] + ', ' + order['shipping_address']['city'] + ', ' + order['shipping_address']['province'] + ', ' + order['shipping_address']['postal_code']) + ', ' + order['shipping_address']['country_code'].upper()
        email = order['customer']['email']
        embed = discord.Embed(
            title='Order information',
            description=f'Order ID: `{order_id}`',
            color=0x2ecc71,
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name='Customer Details', value=f'• :bust_in_silhouette: Name: `{first_name} {last_name}`\n• :mobile_phone: Phone: `{phone}`\n• :e_mail: Email: `{email}`', inline=False)
        embed.add_field(name='Shipping Address', value=f'• :hotel: Address: `{address}`', inline=False)
        embed.set_thumbnail(url='https://i.imgur.com/yFkhOEx.jpg')
        embed.set_footer(text=f'Requseted by {user}', icon_url=avatar_url)
        await interaction.response.send_message(embed=embed)

# On command (/email)
@bot.tree.command(name='email', description='Send an email to the customer')
async def email(interaction: discord.Interaction, order_id: str, *, email_subject: str, email_body: str):
    user = interaction.user
    avatar_url = user.avatar
    r = requests.get(medusa_url + '/store/orders/' + order_id)
    if r.status_code == 404:
        embed = discord.Embed(
            title='Order not found :x:',
            description=f'The order you are looking for with the ID `{order_id}` does not exist',
            color=0xe74c3c,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url='https://i.imgur.com/yFkhOEx.jpg')
        embed.set_footer(text=f'Requseted by {user}', icon_url=avatar_url)
        await interaction.response.send_message(embed=embed)
    elif r.status_code == 200:
        res = r.json()
        customer_email = res['order']['customer']['email']

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
        except Exception as e:
            print(e)
            embed = discord.Embed(
                title='Error :x:',
                description='An error occured while trying to connect to the SMTP server',
                color=0xe74c3c,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_thumbnail(url='https://i.imgur.com/yFkhOEx.jpg')
            embed.set_footer(text=f'Requseted by {user}', icon_url=avatar_url)
            await interaction.response.send_message(embed=embed)
            return
        
        try:
            server.login(email_address, email_password)
        except Exception as e:
            print(e)
            embed = discord.Embed(
                title='Error :x:',
                description='An error occured while trying to login to the SMTP server',
                color=0xe74c3c,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_thumbnail(url='https://i.imgur.com/yFkhOEx.jpg')
            embed.set_footer(text=f'Requseted by {user}', icon_url=avatar_url)
            await interaction.response.send_message(embed=embed)
            return
        embed = discord.Embed(
            title='Email sent :white_check_mark:',
            description=f'An email will be sent to `{customer_email}` shortly',
            color=0x2ecc71,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url='https://i.imgur.com/yFkhOEx.jpg')
        embed.set_footer(text=f'Requseted by {user}', icon_url=avatar_url)
        await interaction.response.send_message(embed=embed)
        try:
            message = 'Subject: {}\n\n{}'.format(email_subject, email_body)
            server.sendmail(email_address, customer_email, message)  
        except Exception as e:
            print(e)
            embed = discord.Embed(
                title='Error :x:',
                description='An error occured while trying to send the email',
                color=0xe74c3c,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_thumbnail(url='https://i.imgur.com/yFkhOEx.jpg')
            embed.set_footer(text=f'Requseted by {user}', icon_url=avatar_url)
            await interaction.response.send_message(embed=embed)
            return

        server.quit()
        
# On command (/coolemail)
@bot.tree.command(name='coolemail', description='Send a cool email to the customer')
async def coolemail(interaction: discord.Interaction, order_id: str, email_subject: str, email_headline: str, email_body: str):
    user = interaction.user
    avatar_url = user.avatar
    r = requests.get(medusa_url + '/store/orders/' + order_id)
    if r.status_code == 404:
        embed = discord.Embed(
            title='Order not found :x:',
            description=f'The order you are looking for with the ID `{order_id}` does not exist',
            color=0xe74c3c,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url='https://i.imgur.com/yFkhOEx.jpg')
        embed.set_footer(text=f'Requseted by {user}', icon_url=avatar_url)
        await interaction.response.send_message(embed=embed)
        return
    elif r.status_code == 200:
        res = r.json()
        customer_email = res['order']['customer']['email']
        customer_first_name = res['order']['customer']['first_name']
        embed.set_thumbnail(url='https://i.imgur.com/yFkhOEx.jpg')
        embed.set_footer(text=f'Requseted by {user}', icon_url=avatar_url)
        await interaction.response.send_message(embed=embed)

        msg = EmailMessage()
        msg['Subject'] = email_subject
        msg['From'] = email_address
        msg['To'] = customer_email
        msg.set_content("Test Mesage")
        html_message = open('template.html').read()
        html_message = html_message.replace('{first_name}', customer_first_name).replace('{email_headline}', email_headline).replace('{email_body}', email_body)
        msg.add_alternative(html_message, subtype='html')
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_address, email_password)
                server.send_message(msg)
        except Exception as e:
            print(e)
            embed = discord.Embed(
                title='Error :x:',
                description='An error occured while trying to send the email',
                color=0xe74c3c,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_thumbnail(url='https://i.imgur.com/yFkhOEx.jpg')
            embed.set_footer(text=f'Requseted by {user}', icon_url=avatar_url)
            await interaction.response.send_message(embed=embed)
            return
        embed = discord.Embed(
            title='Email sent :white_check_mark:',
            description=f'An email will been sent to `{customer_email}` shortly',
            color=0x2ecc71,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url='https://i.imgur.com/yFkhOEx.jpg')
        embed.set_footer(text=f'Requseted by {user}', icon_url=avatar_url)
        await interaction.response.send_message(embed=embed)
        server.send_message(msg)
        server.quit()
        

bot.run(bot_token)