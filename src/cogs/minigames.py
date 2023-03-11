import discord
from discord.ext import commands


from random import choice


class Minigames(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Minigames is online")
    
    @commands.command(aliases = ["8ball", "eightball"])
    async def magic_eightball(self, ctx: commands.context.Context, *, question):
        _8ball = ["It is certain",
                "The KKK has instructed me to say yes",
                "The USSR approves", 
                "It is decidedly so", 
                "Without a doubt", 
                "Yes, definitely",
                "You may rely on it", 
                "As I see it, yes", 
                "Most Likely", 
                "Outlook Good",
                "Yes", 
                "Joe mama so fat Thanos had to clap",
                "Signs point to yes",
                "Maybe you should ask your mother",  
                "Reply hazy, try again", 
                "Ask again later",
                "Better not tell you now", 
                "Cannot predict now", 
                "Concentrate and ask again",
                "Don't count on it", 
                "My reply is no", 
                "My sources say no", 
                "Outlook not so good", 
                "Very Doubtful", 
                "The KKK has instructed me to say no",
                "The USSR does not approve"]

        response = choice(_8ball)

        await ctx.message.delete()
        await ctx.send(response)


async def setup(client):
    await client.add_cog(Minigames(client))
    