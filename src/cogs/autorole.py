import discord
from discord import app_commands
from discord.ext import commands

import json
import requests

class Autorole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Autorole is online")
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        r = requests.get(f"https://mpamias.duckdns.org:9090/api/get_autorole?server_id={member.guild.id}")

        auto_role = r.json().get("autorole")

        role = discord.utils.get(member.guild.roles, id=auto_role)
        await member.add_roles(role)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def set_autorole(self, ctx: commands.context.Context, role: discord.Role):
        await requests.get(f"https://mpamias.duckdns.org:9090/api/set_autorole?server_id={ctx.guild.id}&autorole={role.id}")

        await ctx.send(f"role has been set")

async def setup(client):
    await client.add_cog(Autorole(client))