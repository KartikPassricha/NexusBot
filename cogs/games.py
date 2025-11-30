import discord
from discord.ext import commands
import markovify
import os


class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.models = {}

        # load all models
        for filename in os.listdir("models"):
            if filename.endswith(".json"):
                key = filename.replace(".json", "")
                with open(f"models/{filename}", "r", encoding="utf-8") as f:
                    self.models[key] = markovify.NewlineText.from_json(f.read())


    def generate(self, key):
        if key not in self.models:
            return None

        result = None
        while not result:
            result = self.models[key].make_sentence(tries=50)

        return result

#TRUTH

    @commands.command()
    async def truth(self, ctx, difficulty="easy"):
        difficulty = difficulty.lower()
        key = f"truth_{difficulty}"

        if difficulty == "nsfw" and not ctx.channel.is_nsfw():
            return await ctx.send("❌ NSFW truth can only be used in NSFW channels.")

        result = self.generate(key)
        if not result:
            return await ctx.send("❌ Invalid category.")

        embed = discord.Embed(
            title=f"🟢 TRUTH ({difficulty.upper()})",
            description=result,
            color=0x44ff44
        )
        await ctx.send(embed=embed)

#DARE

    @commands.command()
    async def dare(self, ctx, difficulty="easy"):
        difficulty = difficulty.lower()
        key = f"dare_{difficulty}"

        if difficulty == "nsfw" and not ctx.channel.is_nsfw():
            return await ctx.send("❌ NSFW dare can only be used in NSFW channels.")

        result = self.generate(key)
        if not result:
            return await ctx.send("❌ Invalid category.")

        embed = discord.Embed(
            title=f"🔴 DARE ({difficulty.upper()})",
            description=result,
            color=0xff4444
        )
        await ctx.send(embed=embed)



async def setup(client):
    await client.add_cog(Games(client))
