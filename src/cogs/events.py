import discord
from discord import app_commands
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, client: discord.client.Client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events is online")

    # @commands.Cog.listener()
    # async def ...

async def setup(client):
    await client.add_cog(Events(client))