import discord
from discord.ext import commands
from datetime import datetime
from discord import app_commands


class General(commands.Cog):
    def __init__(self, client):
        self.client = client

#STATUS.....................................................................................................
    @commands.command()
    async def status(self, ctx):
        await ctx.send(
            "**Bot Status:**\n"
            "🎵 Music Commands : ✅\n"
            "⚙️ Moderation Commands : ✅\n"
            "🎮 Game Commands : ✅\n"
            "🤖 AI Chatbot : ❌\n"
        )

#PING................................................................................................................

    @commands.command()
    async def ping(self, ctx):
        latency = round(self.client.latency * 1000)

        if latency <= 50: color = 0x44ff44
        elif latency <= 100: color = 0xffd000
        elif latency <= 200: color = 0xff6600
        else: color = 0x990000

        embed = discord.Embed(
            title="🏓 PING",
            description=f"The ping is **{latency}ms**",
            color=color
        )
        await ctx.send(embed=embed)

#TIME.............................................................................................................

    @commands.command()
    async def time(self, ctx):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        await ctx.send(f"🕒 Current Time: `{current_time}`")

#OWNER................................................................................................................

    @commands.command()
    async def owner(self, ctx):
        embed = discord.Embed(
            title="🤖 Bot Creator",
            description=(
                f"Hello {ctx.author.mention}!\n\n"
                "**Bot created by Kartik.**\n"
                "Started in 2021 as a Truth & Dare bot, now powered by ML, music, moderation & more.\n\n"
                "Use `&help` for all commands."
            ),
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

#SUGGESTION LINK....................................................................................................

    @commands.command()
    async def suggest(self, ctx):
        await ctx.send(
            "📝 Suggestions Form:\n"
            "👉 https://forms.gle/3t1G1gD6ZY8QPMrc9"
        )

#HELP...............................................................................................................

    @commands.command()
    async def help(self, ctx):

        embed = discord.Embed(
            title="🤖 Complete Command List",
            description="All commands grouped by category:",
            color=discord.Color.teal()
        )

        embed.set_thumbnail(url=self.client.user.avatar.url if self.client.user.avatar else None)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)

        embed.add_field(
            name="🎵 Music Commands",
            value=(
                "**`&join`** – Join voice channel\n"
                "**`&leave`** – Leave voice channel\n"
                "**`&play <song>`** – Play music track\n"
                "**`&skip`** – Skip current song\n"
                "**`&pause`** – Pause the song\n"
                "**`&resume`** – Resume playback\n"
                "**`&stop`** – Stop all audio\n"
                "**`&queue`** – View song queue\n\n"

                "**Playlist Commands:**\n"
                "`&create_playlist` – Make playlist\n"
                "`&add_to_playlist <song>` – Add song\n"
                "`&show_playlist` – View songs\n"
                "`&delete_playlist` – Delete playlist\n"
                "`&play_playlist <pos>` – Play playlist\n"
            ),
            inline=False
        )

        embed.add_field(
            name="⚙️ Moderation Commands",
            value=(
                "`&kick @user reason` – Kick member\n"
                "`&ban @user reason` – Ban member\n"
                "`&mute @user d unit reason` – Mute member\n"
                "`&unmute @user` – Unmute member\n"
                "`&addrole @user role` – Give role\n"
                "`&removerole @user role` – Remove role\n"
                "`&add_banned_word w1 w2` – Block words\n"
                "`&remove_banned_word word` – Unblock word\n"
                "`&setroles cmd role1 role2` – Set access\n"
            ),
            inline=False
        )

        embed.add_field(
            name="🎮 Truth & Dare (ML-Based)",
            value=(
                "**Difficulties:** easy / medium / hard /\n"
                "funny / romantic / dark /\n"
                "spicy / cringe / nsfw\n\n"

                "`&truth <type>` – Generate truth\n"
                "`&dare <type>` – Generate dare\n\n"

                "**Examples:**\n"
                "`&truth funny` – Funny truth\n"
                "`&truth spicy` – Spicy truth\n"
                "`&truth nsfw` – NSFW truth\n"
                "`&dare dark` – Dark dare\n"
                "`&dare cringe` – Cringe dare\n"
            ),
            inline=False
        )

        embed.add_field(
            name="ℹ️ General Commands",
            value=(
                "`&ping` – Check latency\n"
                "`&status` – Bot systems status\n"
                "`&owner` – Creator info\n"
                "`&time` – Show time\n"
                "`&suggest` – Suggest features\n"
            ),
            inline=False
        )

        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(General(client))
