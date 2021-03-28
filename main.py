'''
PyShell Discord Bot
Made by: Jason Li

Invite link:
https://discord.com/oauth2/authorize?client_id=825106616826331167&scope=bot&permissions=201587920
'''

import discord
from discord.ext import commands
import os
import subprocess
from datetime import datetime as dt

client = commands.Bot(command_prefix='p! ')

client.remove_command('help')

@client.event
async def on_ready():
    eventTime = str(dt.now())
    print("Bot is online " + eventTime)

    await client.change_presence(activity=discord.Game(name="p! help"))

banned_imports = [
    "pygame",
    "tkinter",
    "pygt5",
    "pygui",
    "pysimplegui",
    "kivy",
]

in_banned = False

@client.event
async def on_message(message):
    global in_banned

    for imports in banned_imports:
        if imports in str(message.content).lower():
            in_banned = True
        else:
            pass
        
    if str(message.channel) == "pyshell" or str(message.channel) == "bot-code":
        if in_banned == False and str(message.author.id) != '825106616826331167':
            inStr = str(message.content)
            f = open("files/pyin.py", "w")
            f.write(inStr)
            f.close()
            with open("files/pyout.txt", "w") as output:
                subprocess.call(["python", "files/pyin.py"], stdout=output)
            output = open("files/pyout.txt", "r")
            outStr = str(output.read())
            if outStr != "":
                await message.channel.send(str(outStr))
            else:
                pass

            confirmStr = (str(message.author) + " ran:") + "\n" + inStr + "\n" + "out:" + "\n" + outStr
            confirmChannel = client.get_channel(825545951003148339)
            print(confirmStr)
            await confirmChannel.send(confirmStr)

            f = open("files/pyin.py", "w")
            f.write("")
            f.close()
        elif in_banned == True and str(message.author.id) != '825106616826331167':
            inStr = str(message.content)
            await message.channel.send("Unavailable command")
            in_banned = False
            print(str(message.author) + " ran:")
            print(inStr)
            print("out: Unavailable command")
        elif str(message.author.id) == '825106616826331167':
            pass
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
    embed=discord.Embed(title="PyShell Bot", description="by: jasonli0616", url="https://pyshell-bot.jasonli0616.repl.co", color=0x00ACEE)
    embed.set_thumbnail(url="https://raw.githubusercontent.com/jasonli0616/PyShell-Discord-Bot/main/pyshell_pfp.png")
    embed.add_field(name="Python", value="Type python code in pyshell or bot-code channel\nChannel named \"pyshell\" or \"bot-code\" required", inline=False)
    embed.add_field(name="Warning", value="Importing GUI libraries will sometimes break the bot, please refrain from doing so.", inline=False)
    embed.add_field(name="Website", value="Visit our website for more info: https://pyshell-bot.jasonli0616.repl.co", inline=False)
    embed.add_field(name="Source code", value="See source code on GitHub: https://github.com/jasonli0616/PyShell-Discord-Bot", inline=False)
    await ctx.send(embed=embed)


client.run(os.getenv("TOKEN"))