import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("---------------------------")
    print("Logged in as: " + bot.user.name)
    print("With ID: " + str(bot.user.id))
    print("---------------------------")

@bot.event
async def on_message(message):
    if(message.author.name != bot.user.name):
        print("------------------------------------------------------")
        print("User " + message.author.display_name + "(" + message.author.name + ")") 
        print("Said: " + message.content)
        print("Channel: " + message.channel.name + " Server: " + message.guild.name)
        await bot.process_commands(message)
        print("------------------------------------------------------")
    else:
        return

for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f'Cogs.{filename[:-3]}')

bot.run('TOKEN') #Replace with your bot's token
