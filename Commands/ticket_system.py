import discord
import asyncio
from datetime import datetime
from discord.ext import commands 
import os 
from config import config
class Tickets(commands.Cog):
    def __init__(self,bot):
        self.bot = bot 

    @commands.slash_command(name="ping",description="""Return Bot's Latency""") #normal ping cmd, make sure to add your guild ids...
    async def ping(self,ctx):
        await ctx.respond(f"**Pong!**\nLatency: {round(self.bot.latency*1000)}ms",ephemeral=True)

    @commands.slash_command(description="""Creates a new convo""") # creating <new> command, use it by writing /new <reason>, I will tell you the use of reason later! make sure u have application.commands scope turned on while inviting the bot
    async def new(self,ctx,reason):
        await ctx.respond("Hold up! working on your request",ephemeral=True)
        categ=discord.utils.get(ctx.guild.categories,name="CONVOS") # selecting the category(by its name)
        try:
            for ch in categ.channels: # using for loop to go through all channels in that category
                if ch.topic==str(ctx.author.id): # checking if author already have a ticket in there, as we added their id as topic
                    return await ch.send("There's already a conversation for you.") # if they have ticket, then mentioning them
            overwrite={
            ctx.guild.default_role:discord.PermissionOverwrite(read_messages=False),
            ctx.me:discord.PermissionOverwrite(read_messages=True),
            ctx.author:discord.PermissionOverwrite(read_messages=True),
            #r1:discord.PermissionOverwrite(read_messages=True)
                } #creating overwrites/permission for channel
            channel=await categ.create_text_channel(name=f"{ctx.author.name}-{ctx.author.discriminator}",overwrites=overwrite,topic=f"{ctx.author.id}") # creating the channel/ticket
            print(channel)
            em=discord.Embed(title='New convo created',
                                description=f"created by {ctx.author.mention}",
                                timestamp=datetime.utcnow(),
                                color=discord.Color.random())
            await asyncio.sleep(3)
            await ctx.respond(f"Click here {channel.mention}",ephemeral=True)
            await channel.send(embed=em)
        except:
            await ctx.respond("Error")
        #r1=ctx.guild.get_role(940569069659242556) FOR MODS 
        


    @commands.slash_command(description="""Closes the convo""")
    async def close(self,ctx): # creating close command
        if ctx.channel.category.name!="CONVOS": # making sure that you cant use this command in any other categs
            return await ctx.respond('Cant use here',ephemeral=True)

        await ctx.respond("Closing Convo!")
        categ=discord.utils.get(ctx.guild.categories,name="CLOSED CONVOS") # selecting the category(by its name)

        ch=ctx.channel
        #r1=ctx.guild.get_role(940569069659242556)

        overwrite={ # creating overwrites
            ctx.guild.default_role:discord.PermissionOverwrite(read_messages=False),
            ctx.me:discord.PermissionOverwrite(read_messages=True),
            #r1:discord.PermissionOverwrite(read_messages=True)
            }

        await ch.edit(category=categ,overwrites=overwrite) # moving the channel to "CLOSED TICKETS"
        mem=await ctx.guild.fetch_member(int(ch.topic)) # getting the member who created the ticket
        os.remove(f"{mem.id}.txt") # deleting the file after uploading

    @commands.slash_command(description="""Delete the covo""")
    async def trash(self,ctx): # creating a command to delete the ticket
        if ctx.channel.category.name!="CLOSED CONVOS": # making sure that this command cant be used in any other channel 
            return await ctx.respond('Cant use in this channel', ephemeral=True)

        await ctx.respond(f'Deleting ticket in {str(config.DELETE_TIME)}')
        await asyncio.sleep(int(config.DELETE_TIME))
        await ctx.channel.delete() # deleting the ticket

def setup(bot):
    bot.add_cog(Tickets(bot))