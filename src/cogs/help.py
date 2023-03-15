import discord
from discord import app_commands
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client: discord.client.Client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help is online")
    
    @commands.command()
    async def help(self, ctx: commands.context.Context):
        help_embed = discord.Embed(title="Help Command", description="help command", color=discord.Color.random())

        help_embed.set_author(name="bot", icon_url=self.client.user.avatar)

        help_embed.add_field(name="set_autorole", value="sets the role to add to users when they join", inline=False)

        help_embed.add_field(name="level", value="shows the users current level", inline=False)
        
        help_embed.add_field(name="8ball", value="8ball minigame ask a question and get  your answer", inline=False)
        
        help_embed.add_field(name="ban", value="bans a user", inline=False)
        help_embed.add_field(name="unban", value="unbans a user", inline=False)
        help_embed.add_field(name="kick", value="kicks a user", inline=False)
        help_embed.add_field(name="clear", value="clears set amount of messages in the chat", inline=False)

        help_embed.add_field(name="set_mute_role", value="sets the role in order to mute people", inline=False)
        help_embed.add_field(name="mute", value="mutes a user", inline=False)
        help_embed.add_field(name="unmute", value="unmutes a user", inline=False)

        help_embed.add_field(name="ping",value="shows the bots latency", inline=False)

        help_embed.add_field(name="change_prefix", value="changes the prefix from !", inline=False)

        help_embed.set_footer(text=f"Requested by <@{ctx.author}>", icon_url=ctx.author.avatar)

        await ctx.send(embed=help_embed)

async def setup(client):
    await client.add_cog(Help(client))