import discord
from discord import app_commands
from discord.ext import commands

# aporofitiras!!

import math
import json
import asyncio
import random

class Level(commands.Cog):
    def __init__(self, client: discord.client.Client):
        self.client = client

        self.client.loop.create_task(self.save())

        with open("./src/data/users.json", "r") as f:
            self.users = json.load(f)

    def level_up(self, author_id: str):
        current_experience = self.users[author_id]["Experience"]
        current_level = self.users[author_id]["Level"]

        if current_experience >= math.ceil(6 * (current_level ** 4) / 2.5):
            self.users[author_id]["Level"] += 1
            return True
        else: return False

    async def save(self):
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            with open("./src/data/users.json", "w") as f:
                json.dump(self.users, f, indent=4)

            await asyncio.sleep(5)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Level is online")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.client.user.id: return

        author_id = str(message.author.id)

        if not author_id in self.users:
            self.users[author_id] = {}
            self.user[author_id]["Level"] = 1
            self.users[author_id]["Experience"] = 0
        
        random_exp = random.randint(5, 15)
        self.users[author_id]["Experience"] += random_exp
        if self.level_up(author_id):
            await message.channel.send(f"{message.author.mention} has leveled up to {self.users[author_id]['Level']}")

    @commands.command(aliases= ["rank", "lvl", "r"])
    async def level(self, ctx: commands.context.Context, user: discord.User = None):
        if user is None:
            user = ctx.author
        elif user is not None:
            user = user
        
        level_card = discord.Embed(title=f"{user.name}'s Level & Experience", color=discord.Color.random())
        level_card.add_field(name="Level:", value=self.users[str(user.id)]["Level"])
        level_card.add_field(name="Experience:", value=self.users[str(user.id)]["Experience"])
        level_card.add_field(name="Required experience for next level:", value=math.ceil(6 * (self.users[str(user.id)]["Level"] ** 4) / 2.5))
        level_card.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)

        await ctx.send(embed=level_card)

async def setup(client):
    await client.add_cog(Level(client))
