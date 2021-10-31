import discord
from discord.ext import commands

import asyncio, os, json, time
import matplotlib.pyplot as plt
import seaborn as sns

from dotenv import load_dotenv
from datetime import datetime
from Naked.toolshed.shell import execute_js

load_dotenv('../.env')
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
sns.set_theme(style="darkgrid")

client = commands.Bot(command_prefix="$", activity = discord.Game(name="💸 Watching the money!"))

@client.event
async def on_ready():
    print('OneWalletWatcher is online!')

@client.command()
async def stats(ctx):
    f = open('stream.json')
    portfolio = json.load(f)[0]['content']

    time = datetime.fromtimestamp(int(portfolio['unix_timestamp']))
    eth_balance = round(float(portfolio['eth_balance']['bal']), 4)
    eth_price = round(float(portfolio['eth_balance']['price']), 2)
    assets_avg_value = round(float(portfolio['assets_data']['total_average_value']), 4)
    address= os.getenv("WALLET_ADDRESS")

    content = (
        "💰 __**PORTFOLIO STATS**__ \n"
        f"*Address:* {address}\n"
        f"*Data Last Updated:* {time}\n\n"
        f"**[WALLET EVALUATION](https://etherscan.io/address/{address})** \n"
        f"**ETH Balance:** {eth_balance} ETH @ ${eth_price} \n"
        f"**USD Approx:** ${round(eth_balance * eth_price, 2)} \n\n"
        f"**[TOKENS AND OTHER ASSETS](https://opensea.io/account)** \n"
        f"**Assets Avg Value:** {assets_avg_value} ETH @ ${eth_price}\n"
        f"**USD Approx:** ${round(assets_avg_value * eth_price, 2)}\n\n"
    )
    embed = discord.Embed(description = content, colour=discord.Colour.green())
    embed.set_footer(text='Powered by Streamr Protocol w/ the Etherscan API, Opensea API, and Coingecko API*',icon_url="https://media.discordapp.net/attachments/896608634023329815/904108992219992134/digital-wallet_1.png")
    await ctx.send(embed=embed)

@client.command()
async def generateWallet(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        content = ("🔐 **YOU REQUESTED A NEW WALLET.** \nRead the following rules carefully."
            " You should not be logged into Discord anywhere else before you use this command."
            " You should NEVER give your private key out to anyone, so write this down in a confidential, safe place immediately before this message self-destructs."
            " By typing `I understand.` below, you assume all responsibility for the security of your newly generated wallet."
            )
        embed = discord.Embed(description = content, colour=discord.Colour.green())
        message = await ctx.author.send(embed=embed)

        try:
            userResponse = await client.wait_for('message', timeout=20)
        except asyncio.TimeoutError:
            await ctx.author.send('🕓 You ran out of time... Run this command again when you are ready.')
            return

        if userResponse.content == 'I understand.':
            file = open('../throwaway.json')
            wallet = json.load(file)
            print(wallet)

            content = (
                f"🔐 __**WALLET GENERATED**__ \n\
                \n*Address:* \n`{wallet['address']}` \
                \n*Private Key:* \n`{wallet['privateKey']}` \
                \n\nThis message is self-destructing in 10 seconds..."
            )
            embed = discord.Embed(description = content, colour=discord.Colour.green())
            message = await ctx.author.send(embed=embed)
            time.sleep(6)
            await message.add_reaction("❌")
            time.sleep(4)
            await message.delete()

def generate_data(num):
    #To Generate
    f = open("../node/config.txt", 'w')
    f.write(str(num))
    f.close()
    execute_js('../node/stream.js')

def generate_graph(type, min):
    f = open('stream.json')
    portfolios = []
    timestamps = []
    total_eth_value = []
    total_usd_value = []

    generate_data(int(min))
    for data in json.load(f): portfolios.append(data['content'])

    # if min > len(portfolios):
    #     print('Repulling for more data points...')
    #     generate_data(int(min))
    #     portfolios = []
    #     for data in json.load(f): portfolios.append(data['content'])

    for portfolio in portfolios:
        timestamps.append(int(portfolio['unix_timestamp']))

        eth_eth_bal = float(portfolio['eth_balance']['bal'])
        asset_eth_bal = float(portfolio['assets_data']['total_average_value'])
        total_eth_bal = eth_eth_bal + asset_eth_bal
        total_eth_value.append(total_eth_bal)

        eth_usd_bal = eth_eth_bal * float(portfolio['eth_balance']['price'])
        asset_usd_bal = asset_eth_bal * float(portfolio['eth_balance']['price'])
        total_usd_bal = eth_usd_bal + asset_usd_bal
        total_usd_value.append(total_usd_bal)


    fig = plt.figure()
    type = type.lower()
    if type == 'usd':
        plt.plot(timestamps, total_usd_value)
        plt.title("Portfolio Value", fontsize=30,fontweight='bold', pad = 10)
        plt.xlabel(f"Time (Last {min} Minutes)", fontsize=12, labelpad = 10)
        plt.ylabel("Value in USD", fontsize=12, labelpad = 5)
    else:
        plt.plot(timestamps, total_eth_value)
        plt.title("Portfolio Value", fontsize=30, fontweight='bold', pad = 10)
        plt.xlabel(f"Time (Last {min} Minutes)", fontsize=22, labelpad = 10)
        plt.ylabel("Value in ETH", fontsize=12, labelpad = 5)
    plt.xticks([])
    address = os.getenv("WALLET_ADDRESS")
    plt.savefig('graph.png')
    return total_eth_value, total_usd_value

@client.command()
async def graph(ctx, min=60, type='usd'):
    total_eth_value, total_usd_value = generate_graph(type, int(min))
    chart = discord.File("graph.png", filename="graph.png")
    await ctx.send(file=chart)

    address = os.getenv("WALLET_ADDRESS")

    if type == 'usd': percent_change = ((total_eth_value[-1] - total_eth_value[0]) / total_eth_value[-1]) * 100
    else: percent_change = ((total_usd_value[-1] - total_usd_value[0]) / total_usd_value[-1]) * 100
    if percent_change >= 0: sign = '+'
    else: sign = ''

    content = (
        f"📈 __**PORTFOLIO PERFORMANCE (Last {min} Minutes)**__ \n\
        \n*Address:* \n`{address}` \n\
        \n*Average Portfolio Value:* \n `{round(sum(total_eth_value)/len(total_eth_value), 4)} ETH` or `{round(sum(total_usd_value)/len(total_usd_value), 4)} USD` \
        \n\nLast {min} Minutes: {sign}{round(percent_change, 4)}%"
    )
    embed = discord.Embed(description = content, colour=discord.Colour.green())
    message = await ctx.send(embed=embed)

@client.command()
async def news(ctx,):
    total_eth_value, total_usd_value = generate_graph(type, int(min))
    chart = discord.File("graph.png", filename="graph.png")
    await ctx.send(file=chart)

    address = os.getenv("WALLET_ADDRESS")

    if type == 'usd': percent_change = ((total_eth_value[-1] - total_eth_value[0]) / total_eth_value[-1]) * 100
    else: percent_change = ((total_usd_value[-1] - total_usd_value[0]) / total_usd_value[-1]) * 100
    if percent_change >= 0: sign = '+'
    else: sign = ''

    content = (
        f"📈 __**PORTFOLIO PERFORMANCE (Last {min} Minutes)**__ \n\
        \n*Address:* \n`{address}` \n\
        \n*Average Portfolio Value:* \n `{round(sum(total_eth_value)/len(total_eth_value), 4)} ETH` or `{round(sum(total_usd_value)/len(total_usd_value), 4)} USD` \
        \n\nLast {min} Minutes: {sign}{round(percent_change, 4)}%"
    )
    embed = discord.Embed(description = content, colour=discord.Colour.green())
    message = await ctx.send(embed=embed)

client.run(BOT_TOKEN)
