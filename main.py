import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.all()
client = commands.Bot(command_prefix='&', intents=intents)
client.remove_command("help")
intents.message_content = True

@client.event
async def on_ready():
    print("BOT is online!")
    await client.change_presence(activity=discord.Game("&help"))

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded: {filename}")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Unknown command. Use `&help`")
    else:
        raise error

client.run("1111MTE1NDc3MzM5MjEzODk2OTIxMA.Gl4ogM.GSipAtofc9tShdBcTvFeees-IzrHQ259MeCKzc1111")
