import discord
from discord import app_commands
from discord.ext import commands

import json
import requests

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Welcome is online")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        r = await requests.get(f"https://mpamias.duckdns.org:9090/api/get_message?server_id={member.guild.id}")
        message = r.json().get("message")
        r = await requests.get(f"https://mpamias.duckdns.org:9090/api/get_channel?server_id={member.guild.id}")
        channel = r.json().get("message")

        if message == None or channel == None:
            return

        welcome_embed = discord.Embed(title=f"Welcome to {member.guild.name}", description=f"Welcome to the server! you are member {member.guild.member_count}!", color=discord.Color.random())
        welcome_embed.add_field(name=f"Welcome to the server!", value=channel)
        welcome_embed.set_footer(text="Glad you joined", icon_url=member.avatar)
        
        channel = discord.utils.get(member.guild.channels, id=channel)
        await channel.send(embed=welcome_embed)
    
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
        await requests.get(f"https://mpamias.duckdns.org:9090/api/set_autorole?server_id={ctx.guild.id}&autorole={role.id}")

        await ctx.send("role has been accepted")

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def message(self, ctx: commands.context.Context, *, msg: str):
        await requests.get(f"https://mpamias.duckdns.org:9090/api/set_message?server_id={ctx.guild.id}&message={msg}")

        await ctx.send("message has been set")

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx: commands.context.Context, channel: discord.channel.TextChannel):
        await requests.get(f"https://mpamias.duckdns.org:9090/api/set_channel?server_id={ctx.guild.id}&channel={channel.id}")

        await ctx.send("channel has been set")

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def image(self, ctx: commands.context.Context, img):
        await requests.get(f"https://mpamias.duckdns.org:9090/api/set_image?server_id={ctx.guild.id}&image={str(img)}")

        await ctx.send("image has been set")


async def setup(client):
    await client.add_cog(Welcome(client))