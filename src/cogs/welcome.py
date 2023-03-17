import discord
from discord import app_commands
from discord.ext import commands

import json
import asyncio

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.client.loop.create_task(self.save())

        with open("./src/data/welcome.json", "r") as f:
            self.data = json.load(f)



    async def save(self):
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            with open("./src/data/welcome.json", "w") as f:
                json.dump(self.data, f, indent=4)

            await asyncio.sleep(5)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Welcome is online")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):        
        self.data[str(guild.id)] = {}
        self.data[str(guild.id)]["Channel"] = None
        self.data[str(guild.id)]["Message"] = None
        self.data[str(guild.id)]["Autorole"] = None
        self.data[str(guild.id)]["ImageUrl"] = None

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        self.data.pop(str(guild.id))
    
    @commands.group(name='welcome', invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx:commands.context.Context):
        info_embed = discord.Embed(
            title="Welcome System Setup",
            description="Create a unique welcome system for your server!",
            color=discord.Color.random()
        )

        info_embed.add_field(
            name="autorole",
            value="Set an automatic role so when a user joins they will receive it automatically",
            inline=False
        )

        info_embed.add_field(
            name="message",
            value="Set a message to be include in your welcome card",
            inline=False
        )

        info_embed.add_field(
            name="channel",
            value="Set a channel for your welcome card to be send in",
            inline=False
        )
        
        info_embed.add_field(
            name="img",
            value="Set an image or a gif to be sent  with the welcome card",
            inline=False
        )

        await ctx.send(embed=info_embed)

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx: commands.context.Context, role: discord.Role):
        self.data[str(ctx.guild.id)]["Autorole"] = role.id

        await ctx.send("role has been accepted")

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def message(self, ctx: commands.context.Context, *, msg: str):
        self.data[str(ctx.guild.id)]["Message"] = msg

        await ctx.send("message has been set")

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx: commands.context.Context, channel: discord.channel.TextChannel):
        self.data[str(ctx.guild.id)]["Channel"] = channel.id

        await ctx.send("channel has been set")

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def image(self, ctx: commands.context.Context, img):
        self.data[str(ctx.guild.id)]["ImageUrl"] = str(img)

        await ctx.send("image has been set")


async def setup(client):
    await client.add_cog(Welcome(client))