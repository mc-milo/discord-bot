import discord
from discord.ext import commands


import json
import requests

class Mute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Mute is online")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_mute_role(self, ctx: commands.context.Context, role: discord.Role):
        requests.get(f"https://mpamias.duckdns.org:9090/api/set_mute?server_id={ctx.guild.id}&mute={role.id}")
    
        await ctx.send(f"role has been set")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx: commands.context.Context, member: discord.Member):
        r = requests.get(f"https://mpamias.duckdns.org:9090/api/get_mute?server_id={ctx.guild.id}")

        role = r.json().get("message")
        
        mute_role = discord.utils.get(ctx.guild.roles, id=role)
        
        await member.add_roles(mute_role)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx: commands.context.Context, member: discord.Member):
        r = requests.get(f"https://mpamias.duckdns.org:9090/api/get_mute?server_id={ctx.guild.id}")
        
        role = r.json().get("message")
        
        mute_role = discord.utils.get(ctx.guild.roles, id=role)
        
        await member.remove_roles(mute_role)

async def setup(client):
    await client.add_cog(Mute(client))
