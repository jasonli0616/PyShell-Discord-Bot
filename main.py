'''
PyShell Discord Bot

Made by: Jason Li
'''

# Invite link:
# https://discord.com/oauth2/authorize?client_id=825106616826331167&scope=bot&permissions=76800

import discord
from discord.ext import commands
import os
import subprocess
from datetime import datetime as dt

client = commands.Bot(command_prefix='p!')

client.remove_command('help')

@client.event
async def on_ready():
    eventTime = str(dt.now())
    print("Bot is online " + eventTime + "UTC")

    await client.change_presence(activity=discord.Game(name="p!"))

banned_imports = [
    "pygame",
    "tkinter",
    "pygt5",
    "pygui",
]

channels = [
    # channel id int here
]

in_banned = False
code_channel = False

@client.event
async def on_message(message):
    global in_banned, code_channel

    for imports in banned_imports:
        if imports in str(message.content).lower():
            in_banned = True
        else:
            in_banned = False
    
    for channelIDs in channels:
        if channelIDs == message.channel.id:
            code_channel = True
        else:
            code_channel = False
        
    if code_channel == True and message.author.id != client.user.id and in_banned == False:
        inStr = str(message.content)
        f = open("files/pyin.py", "w")
        f.write(inStr)
        f.close()
        with open("files/pyout.txt", "w") as output:
            subprocess.call(["python", "files/pyin.py"], stdout=output)
        output = open("files/pyout.txt", "r")
        outStr = output.read()
        await message.channel.send(outStr)
        print("ran:")
        print(inStr)
        print("out:")
        print(outStr)
        f = open("files/pyin.py", "w")
        f.write("")
        f.close()
    else:
        pass

    await client.process_commands(message)

@client.command()
async def test(ctx):
    eventTime = str(dt.now())
    embedTitle = "Bot is online " + eventTime + "UTC"
    embed = discord.Embed(title=embedTitle)
    await ctx.send(embed=embed)

@client.command()
async def help(ctx, args=None):
    embed=discord.Embed(title="PyShell Bot", description="by: jasonli0616\nWhat can I do?", color=0x00ACEE)
    embed.set_thumbnail(url="https://raw.githubusercontent.com/jasonli0616/PyShell-Discord-Bot/main/pyshell_pfp.png")
    embed.add_field(name="Python", value="Type python code in bot-code or bot-commands channel", inline=False)
    embed.add_field(name="Warning", value="Importing GUI libraries will sometimes break the bot, please refrain from doing so.", inline=False)
    await ctx.send(embed=embed)


client.run(os.getenv("TOKEN"))