from discord.ext import commands
import os
import discord
from config import config
import json 

if __name__ == "__main__":
  import logging
  bot = commands.Bot(command_prefix=config.BOT_PREFIX,
                   pm_help=True, intents=discord.Intents.all())
  logger = logging.getLogger('discord')
  logger.setLevel(logging.DEBUG)
  handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
  handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
  logger.addHandler(handler)

  if config.BOT_TOKEN == "":
      print("Error: No bot token!")
      exit
  cogs = []
  for fn in os.listdir("./Commands"):
    if fn.endswith(".py"):
        try:
            bot.load_extension(f"Commands.{fn[:-3]}")
            cogs.append(f"Commands.{fn[:-3]}")
        except Exception as e:
            continue

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=config.STATUS_BOT.format(any=config.BOT_PREFIX)))
    print(config.STARTUP_COMPLETE_MESSAGE.format(botName=bot.user.name))
bot.run(config.BOT_TOKEN, reconnect=True)
