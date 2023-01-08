import discord
from discord.ext import commands
from openAiApi import generateResponse
from db import (getPrev,addEntry)
class Convo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        print(message.channel.category.name)
        if message.channel.category.name == 'CONVOS':
            channelID: str = str(message.channel.id)
            userID: str = str(message.author.id)
            prevConvo = await getPrev(userID=userID,channelID=channelID) 
            response: str = generateResponse(question=message.content,temp=1,prevConvo=prevConvo)
            if response != None:
                try:
                    await message.channel.send(response.strip())
                except Exception as e:
                    print(e)
                    print('Exception while trying to send message response.')
            try:
                await addEntry(userID=userID,message=message.content,channelID=channelID)
            except Exception as e:
                print(e)
                print('Could not add conversation history.')


def setup(bot):
    bot.add_cog(Convo(bot))

