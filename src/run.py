import discord
from discord.ext import commands, tasks

import os
import asyncio
import requests

from itertools import cycle

from dotenv import load_dotenv

load_dotenv("./src/data/.env")

def get_server_prefix(client, message: discord.Message):
    r = requests.get(f"https://mpamias.duckdns.org:9090/api/get_prefix?server_id={message.guild.id}")

    r.json().get("prefix")
    return r.json().get("prefix")


client = commands.Bot(
    command_prefix=get_server_prefix,
    intents=discord.Intents.all(),
    case_insensitive= True
)

client.remove_command("help")

bot_status = cycle(["Hi", "Hello", "Mpamies", "AAAAAAA", "!help"])

@tasks.loop(minutes=1)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

@client.event
async def on_ready():
    await client.tree.sync()
    print("bot ready")
    change_status.start()

@client.event
async def on_guild_join(guild: discord.Guild):
    requests.get(f"https://mpamias.duckdns.org:9090/api/join_guild?server_id={guild.id}")

@client.event
async def on_guild_remove(guild):
    requests.get(f"https://mpamias.duckdns.org:9090/api/remove_guild?server_id={guild.id}")

@client.command()
async def change_prefix(ctx: commands.context.Context, *, prefix: str):
    requests.get(f"https://mpamias.duckdns.org:9090/api/set_prefix?server_id={ctx.guild.id}&prefix={prefix}")

    ctx.send(f"prefix changed to {prefix}")

@client.tree.command(name="ping", description="shows bot's latency in ms.")
async def ping(interaction: discord.Interaction):
    bot_latency = round(client.latency * 1000)

    await interaction.response.send_message(f"{bot_latency} ms", ephemeral=True)  # only the user who run the command can see this message

async def load():
    for filename in os.listdir("./src/cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load()
        await client.start(os.getenv("token"))

asyncio.run(main())