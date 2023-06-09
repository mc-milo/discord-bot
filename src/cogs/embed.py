import discord
from discord import app_commands
from discord.ext import commands

class Emb(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Emb is online")

    @commands.command()
    async def embed(self, ctx):
        embed_message = discord.Embed(
                                    title="Title of embed", 
                                    description="Description of embed", 
                                    color=discord.Color.random() # ctx.author.color as well
                                    ) 
        
        embed_message.set_author(name=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)
        embed_message.add_field(name="field name", value="field value", inline=False)
        embed_message.set_thumbnail(url=ctx.guild.icon)
        embed_message.set_image(url=ctx.guild.icon)
        embed_message.set_footer(text="this is the footer", icon_url=ctx.author.avatar)

        await ctx.send(embed = embed_message)

    @app_commands.command()
    async def embed(self, interaction: discord.Interaction):
        embed_message = discord.Embed(
                                    title="Title of embed", 
                                    description="Description of embed", 
                                    color=discord.Color.random() # interaction.user.color as well
                                    ) 
        
        embed_message.set_author(name=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar)
        embed_message.add_field(name="field name", value="field value", inline=False)
        embed_message.set_thumbnail(url=interaction.guild.icon)
        embed_message.set_image(url=interaction.guild.icon)
        embed_message.set_footer(text="this is the footer", icon_url=interaction.user.avatar)

        await interaction.response.send_message(embed=embed_message, ephemeral=True)
    
async def setup(client):
    await client.add_cog(Emb(client))
