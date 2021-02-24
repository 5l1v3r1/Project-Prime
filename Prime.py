import base64

import discord
import requests
from discord.ext import commands

# Variables enterprise
prefix = "!"
token = "bot token here mate"
embedColor = discord.Colour.gold()

# Bot enterprise
bot = commands.Bot(command_prefix=prefix, help_command=None)


# on_connect enterprise
@bot.event
async def on_connect():
    print(f"{bot.user.name} is now online!")


# Command enterprise

# Help Command
@bot.command(aliases=['help'])
async def prime(ctx):
    embed=discord.Embed(title="Commands are listed below!", color=embedColor)
    embed.add_field(name="**mcserver**", value=f"Gives information about a minecraft server, example: {prefix}mcserver hypixel.net")
    embed.add_field(name="**mcuser**", value=f"Gives information about a minecraft account, example: {prefix}mcuser Notch")
    embed.add_field(name="**ipinfo**", value=f"Gives information about a ip address, example: {prefix}ipinfo 1.1.1.1")
    embed.add_field(name="**base64**", value=f"Encode and Decode data with base64, example: {prefix}base64 type(encode or decode) message")
    await ctx.send(embed=embed)


# IPInfo Command
@bot.command()
async def ipinfo(ctx, ip):
    try:
        p = requests.get(f"http://ip-api.com/json/{ip}")
        if '"status":"success"' in p.text:
            embed = discord.Embed(title="**IPINFO**", description=f"IP • **{ip}**\n"
                                                                  f" Country • **{p.json()['country']}**\n"
                                                                  f" Country Code • **{p.json()['countryCode']}**\n"
                                                                  f" Region • **{p.json()['region']}**\n"
                                                                  f" Region Name • **{p.json()['regionName']}**\n"
                                                                  f" City • **{p.json()['city']}**\n"
                                                                  f" Timezone • **{p.json()['timezone']}**\n"
                                                                  f" Zip • **{p.json()['zip']}**\n"
                                                                  f" ISP • **{p.json()['isp']}**", color=embedColor)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Failed Exception", description="The ip address is invalid.", color=embedColor)
            await ctx.send(embed=embed)
    except Exception as e:
        print(f"Error occurred: {e}")


# MCUser Command
@bot.command()
async def mcuser(ctx, username):
    try:
        names = []
        names.clear()
        req = requests.get(f'https://playerdb.co/api/player/minecraft/{username}')
        if 'code":"player.found"' in req.text:
            embed = discord.Embed(title=f"**MC INFORMATION | {username}**", color=embedColor)
            embed.add_field(name="**Full UUID:**", value=f"{req.json()['data']['player']['id']}", inline=False)
            embed.add_field(name="**Trimmed UUID:**", value=f"{req.json()['data']['player']['raw_id']}", inline=False)
            for name in req.json()['data']['player']['meta']['name_history']:
                names.append(name['name'])
            embed.add_field(name="**Past Usernames**", value=f"({len(names)}): {names}", inline=False)
            embed.set_thumbnail(url="https://crafatar.com/avatars/" + f"{req.json()['data']['player']['id']}")
            await ctx.send(embed=embed)
    except Exception as e:
        print(f"Error occurred: {e}")


# MCServer Command
@bot.command()
async def mcserver(ctx, domain):
    p = requests.get(f'https://api.mcsrvstat.us/2/{domain}')
    try:
        if 'online":true' in p.text:
            embed = discord.Embed(title=f"**MC SERVER INFORMATION | {domain}**", color=embedColor)
            embed.add_field(name="IP", value=f"{p.json()['ip']}", inline=False)
            embed.add_field(name="Port:", value=f"{p.json()['port']}", inline=False)
            embed.add_field(name="Version:", value=f"{p.json()['version']}", inline=False)
            embed.add_field(name="Players:", value=f"{p.json()['players']['online']}/{p.json()['players']['max']}",
                            inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"**{domain} is offline...",
                                  description="The server domain you have put is offline or invalid.", color=embedColor)
            await ctx.send(embed=embed)
    except Exception as e:
        print(f"Error occurred: {e}")


# Base64 Command
@bot.command(name="base64")
async def base_64(ctx, basetype, *, data):
    try:
        if basetype == "encode":
            encode = base64.b64encode(data.encode()).decode()
            embed = discord.Embed(title="**ENCODED**", description=f"{encode}", color=embedColor)
            await ctx.send(embed=embed)
        elif basetype == "decode":
            decode = base64.b64decode(data).decode()
            embed = discord.Embed(title="**DECODED**", description=f"{decode}", color=embedColor)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Failed Exception",
                                  description="Base type is invalid! Please use one of the following types: encode, "
                                              "decode",
                                  color=embedColor)
            await ctx.send(embed=embed)
    except Exception as e:
        print(f"Error ccurred: {e}")


# ErrorHandler enterprise
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument! Please try again!")
    else:
        await ctx.send(error)


# Login enterprise
bot.run(token, bot=True)
