import discord
from discord.ext import commands, tasks

import os
import asyncio
import json


from itertools import cycle


def get_server_prefix(client, message):
    with open("./src/data/prefixes.json", "r") as f:
        prefix = json.load(f)

    return prefix[str(message.guild.id)]


client = commands.Bot(
    command_prefix=get_server_prefix,
    intents=discord.Intents.all()
)

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
async def on_guild_join(guild):
    with open("./src/data/prefixes.json", "r") as f:
        prefix = json.load(f)

    prefix[str(guild.id)] = "!"

    with open("./src/data/prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)

    with open("./src/data/muted.json", "r") as f:
        mute_role = json.load(f)

        mute_role[str(guild.id)] = None
    with open("./src/data/muted.json", "w"):
        json.dump(mute_role, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open("./src/data/prefixes.json", "r") as f:
        prefix = json.load(f)

    prefix.pop(str(guild.id))

    with open("./src/data/prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)
    
    with open("./src/data/muted.json", "r") as f:
        mute_role = json.load(f)

        mute_role.pop(str(guild.id))
    
    with open("./src/data/muted.json", "w") as f:
        json.dump(mute_role, f, indent=4)

@client.command()
async def change_prefix(ctx: commands.context.Context, *, prefix: str):
    with open("./src/data/prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("./src/data/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
    await ctx.send(f"Prefix changed to {prefix}")

@client.tree.command(name="ping", description="shows bot's latency in ms.")
async def ping(interaction: discord.Interaction):
    bot_latency = round(client.latency * 1000)

    await interaction.response.send_message(f"{bot_latency} ms", ephemeral=True) 
                                                                    # only the user who run the command can see this message

async def load():
    for filename in os.listdir("./src/cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load()
        await client.start(open("./src/data/token.0", "r").read())

asyncio.run(main())