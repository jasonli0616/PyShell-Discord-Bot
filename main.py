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

banned_imports = [
    "pygame",
    "tkinter",
    "pygt5",
    "pygui",
    "pysimplegui",
    "kivy",
    "rm",
    "rmdir",
]

in_banned = False

@client.event
async def on_message(message):
    global in_banned

    # checks if anything in banned_imports list is in message
    for imports in banned_imports:
        if imports in str(message.content).lower():
            in_banned = True
        else:
            pass
        
    #if in correct channel
    if str(message.channel) == "pyshell" or str(message.channel) == "bot-code":
        #if message does not contain anything in banned_imports list and if message is not sent by itself
        if in_banned == False and str(message.author.id) != '825106616826331167':
            inStr = str(message.content)
            #writes message sent to a .py file
            f = open("files/pyin.py", "w")
            f.write(inStr)
            f.close()
            #runs that .py file in terminal and writes the terminal output into .txt file
            with open("files/pyout.txt", "w") as output:
                subprocess.call(["python", "files/pyin.py"], stdout=output)
            output = open("files/pyout.txt", "r")
            #reads terminal output .txt file  and sends it into same channel as original message
            outStr = str(output.read())
            if outStr != "":
                await message.channel.send(str(outStr))
            else:
                pass

        #if message DOES contain anything in banned_imports list and if message is not sent by itself
        elif in_banned == True and str(message.author.id) != '825106616826331167':
            inStr = str(message.content)
            #sends unavailable message to same channel as original message
            await message.channel.send("Unavailable command")
            in_banned = False
        
        #if message is sent by itself, does nothing
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


client.run(os.getenv("TOKEN"))
