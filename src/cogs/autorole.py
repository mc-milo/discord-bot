import discord
from discord import app_commands
from discord.ext import commands

import json

class Autorole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Autorole is online")
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        with open("./src/data/autorole.json", "r") as f:
            auto_role = json.load(f)

        role = discord.utils.get(member.guild.roles, id=auto_role[str(member.guild.id)])
        await member.add_roles(role)


    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        with open("./src/data/autorole.json", "r") as f:
            autorole = json.load(f)
        
        autorole[str(guild.id)] = None
    
        with open("./src/data/autorole.json", "w") as f:
            json.dump(autorole, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        with open("./src/data/autorole.json", "r") as f:
            autorole = json.load(f)
        
        autorole.pop(str(guild.id))
    
        with open("./src/data/autorole.json", "w") as f:
            json.dump(autorole, f, indent=4)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def set_autorole(self, ctx: commands.context.Context, role: discord.Role):
        with open("./src/data/autorole.json", "r") as f:
            autorole = json.load(f)

        autorole[str(ctx.guild.id)] = role.id
    
        with open("./src/data/autorole.json", "w") as f:
            json.dump(autorole, f, indent=4)

async def setup(client):
    await client.add_cog(Autorole(client))