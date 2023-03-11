import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation is online")
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.context.Context, count: int):
        await ctx.channel.purge(limit=count)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.context.Context, member: discord.Member, *, reason: str = None):
        await ctx.guild.kick(member, reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.context.Context, member: discord.Member, *, reason: str = None):
        await ctx.guild.ban(member, reason=reason)

    @commands.command(name = "unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: commands.context.Context, userID):
        user = discord.Object(id=userID)
        await ctx.guild.unban(user)

async def setup(client):
    await client.add_cog(Moderation(client))