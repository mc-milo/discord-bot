import discord
from discord.ext import commands


import json

class Mute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Mute is online")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        with open("./src/data/muted.json", "r") as f:
            mute_role = json.load(f)
        
        mute_role[str(guild.id)] = None
    
        with open("./src/data/muted.json", "w") as f:
            json.dump(mute_role, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        with open("./src/data/muted.json", "r") as f:
            mute_role = json.load(f)
        
        mute_role.pop(str(guild.id))
    
        with open("./src/data/muted.json", "w") as f:
            json.dump(mute_role, f, indent=4)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_mute_role(self, ctx, role: discord.Role):
        with open("./src/data/muted.json", "r") as f:
            mute_role = json.load(f)

        mute_role[str(ctx.guild.id)] = role.id
    
        with open("./src/data/muted.json", "w") as f:
            json.dump(mute_role, f, indent=4)
    
        await ctx.send(f"role has been set")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx: commands.context.Context, member: discord.Member):
        with open("./src/data/muted.json", "r") as f:
            role = json.load(f)
        
            mute_role = discord.utils.get(ctx.guild.roles, id=role[str(ctx.guild.id)])
        
        await member.add_roles(mute_role)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx: commands.context.Context, member: discord.Member):
        with open("./src/data/muted.json", "r") as f:
            role = json.load(f)

            mute_role = discord.utils.get(ctx.guild.roles, id=role[str(ctx.guild.id)])
        
        await member.remove_roles(mute_role)

async def setup(client):
    await client.add_cog(Mute(client))
