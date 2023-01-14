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
            userName: str = str(message.author.name)
            msg: str = (message.content).strip()
            prevConvo = await getPrev(userID=userID,channelID=channelID,userName=userName) 
            if prevConvo == None or prevConvo == '': response: str = generateResponse(question=f'{userName}:{msg}\nAI:\n',temp=1,prevConvo=prevConvo,userName=userName)
            else: response: str = generateResponse(question=msg,temp=1,prevConvo=prevConvo,userName=userName)
            if response != None:
                try:
                    response = response.strip()
                    await message.channel.send(response.strip())
                except Exception as e:
                    print(e)
                    print('Exception while trying to send message response.')
            try:
                await addEntry(userID=userID,message=msg,channelID=channelID,response=response)
            except Exception as e:
                print(e)
                print('Could not add conversation history.')


def setup(bot):
    bot.add_cog(Convo(bot))

