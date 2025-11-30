import discord
from discord.ext import commands
import json, asyncio, os, re

BANNED_WORDS_FILE = "data/banned_words.json"
WARNINGS_FILE = "data/warnings.json"

def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(path, data):
    os.makedirs("data", exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# Load stored data

banned_words_per_guild = load_json(BANNED_WORDS_FILE)
warnings = load_json(WARNINGS_FILE)

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.allowed_roles = {
            "kick": {},
            "ban": {},
            "mute": {},
            "addrole": {},
            "removerole": {},
            "unmute": {}
        }

#PERMISSION CHECK

    def has_allowed_role(self, ctx, command):
        creator_role = ctx.guild.owner
        allowed = self.allowed_roles.get(command, [])
        return ctx.author == creator_role or any(role.id in allowed for role in ctx.author.roles)

#SET ROLES

    @commands.command()
    async def setroles(self, ctx, command: str, *roles: discord.Role):
        if ctx.author != ctx.guild.owner:
            return await ctx.send("Only the **server owner** can use this.")

        command = command.lower()
        if command not in self.allowed_roles:
            return await ctx.send("Invalid command name.")

        self.allowed_roles[command] = [r.id for r in roles]

        await ctx.send(
            "✅ Roles allowed for `{}`: {}".format(
                command,
                ", ".join([r.name for r in roles])
            )
        )

#KICK / BAN

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if not self.has_allowed_role(ctx, "kick"):
            return await ctx.send("❌ You do not have permission.")

        if not reason:
            return await ctx.send("Provide a reason.")

        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} kicked. Reason: {reason}")

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if not self.has_allowed_role(ctx, "ban"):
            return await ctx.send("❌ You do not have permission.")

        if not reason:
            return await ctx.send("Provide a reason.")

        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} banned. Reason: {reason}")

#MUTE

    @commands.command()
    async def mute(self, ctx, member: discord.Member, duration: int = None,
                   time_unit: str = None, *, reason=None):

        if not self.has_allowed_role(ctx, "mute"):
            return await ctx.send("❌ You do not have permission.")

        if not duration or not time_unit:
            return await ctx.send("Usage: `&mute @user <duration> <seconds/minutes/hours/days> <reason>`")

        if not reason:
            return await ctx.send("Provide a reason.")

#Find or create Muted role

        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False)

        await member.add_roles(mute_role)
        await ctx.send(f"🔇 {member.mention} muted for {duration} {time_unit}. Reason: {reason}")

        await asyncio.sleep(self.convert_to_seconds(duration, time_unit))

        await member.remove_roles(mute_role)
        await ctx.send(f"🔊 {member.mention} unmuted.")


    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        if not self.has_allowed_role(ctx, "unmute"):
            return await ctx.send("❌ You do not have permission.")

        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            return await ctx.send("Muted role does not exist.")

        if mute_role not in member.roles:
            return await ctx.send(f"{member.mention} is not muted.")

        await member.remove_roles(mute_role)
        await ctx.send(f"🔊 {member.mention} has been unmuted.")

#ADD / REMOVE ROLE

    @commands.command()
    async def addrole(self, ctx, member: discord.Member, role: discord.Role):
        if not self.has_allowed_role(ctx, "addrole"):
            return await ctx.send("❌ You do not have permission.")

        await member.add_roles(role)
        await ctx.send(f"🟢 Added role `{role.name}` to {member.mention}")

    @commands.command()
    async def removerole(self, ctx, member: discord.Member, role: discord.Role):
        if not self.has_allowed_role(ctx, "removerole"):
            return await ctx.send("❌ You do not have permission.")

        await member.remove_roles(role)
        await ctx.send(f"🔴 Removed role `{role.name}` from {member.mention}")

 #BANNED WORD SYSTEM

    def contains_banned_word(self, text, guild_id):
        banned_list = banned_words_per_guild.get(str(guild_id), [])
        for word in banned_list:
            if re.search(rf"\b{re.escape(word)}\b", text, re.IGNORECASE):
                return True
        return False

#MULTIPLE WORDS ADDED AT ONCE

    @commands.command()
    async def add_banned_word(self, ctx, *words):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send("❌ Administrator only.")

        gid = str(ctx.guild.id)
        banned_words_per_guild.setdefault(gid, [])

        added_words = []

        for w in words:
            w = w.lower()
            if w not in banned_words_per_guild[gid]:
                banned_words_per_guild[gid].append(w)
                added_words.append(w)

        save_json(BANNED_WORDS_FILE, banned_words_per_guild)

        if added_words:
            await ctx.send("🚫 Added banned words: " + ", ".join(added_words))
        else:
            await ctx.send("⚠️ All words were already banned.")

#MULTIPLE WORDS REMOVED AT ONCE

    @commands.command()
    async def remove_banned_word(self, ctx, *words):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send("❌ Administrator only.")

        gid = str(ctx.guild.id)
        removed = []

        for w in words:
            w = w.lower()
            if w in banned_words_per_guild.get(gid, []):
                banned_words_per_guild[gid].remove(w)
                removed.append(w)

        save_json(BANNED_WORDS_FILE, banned_words_per_guild)

        if removed:
            await ctx.send("🟢 Removed banned words: " + ", ".join(removed))
        else:
            await ctx.send("⚠️ None of the words were banned.")

#WARNING COUNTER SYSTEM

    def add_warning(self, guild_id, user_id):
        gid, uid = str(guild_id), str(user_id)

        warnings.setdefault(gid, {})
        warnings[gid].setdefault(uid, 0)

        warnings[gid][uid] += 1
        save_json(WARNINGS_FILE, warnings)

        return warnings[gid][uid]

    def reset_warnings(self, guild_id, user_id):
        gid, uid = str(guild_id), str(user_id)
        if gid in warnings and uid in warnings[gid]:
            warnings[gid][uid] = 0
            save_json(WARNINGS_FILE, warnings)

#MESSAGE LISTENER

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        guild_id = message.guild.id
        user_id = message.author.id

#BANNED WORD DETECTION
        if self.contains_banned_word(message.content, guild_id):
            await message.delete()

            warn_count = self.add_warning(guild_id, user_id)

            if warn_count < 5:
                return await message.channel.send(
                    f"{message.author.mention} ⚠️ Warning {warn_count}/5: Avoid banned words."
                )

#AUTO-MUTE AFTER 5 WARNINGS
            self.reset_warnings(guild_id, user_id)

            mute_role = discord.utils.get(message.guild.roles, name="Muted")
            if not mute_role:
                mute_role = await message.guild.create_role(name="Muted")
                for channel in message.guild.channels:
                    await channel.set_permissions(mute_role, send_messages=False)

            await message.author.add_roles(mute_role)
            await message.channel.send(f"🔇 {message.author.mention} auto-muted for 1 day.")

            await asyncio.sleep(86400)
            await message.author.remove_roles(mute_role)
            await message.channel.send(f"🔊 {message.author.mention} auto-unmuted.")

    def convert_to_seconds(self, duration, unit):
        unit = unit.lower()
        if unit in ["second", "seconds"]:
            return duration
        if unit in ["minute", "minutes"]:
            return duration * 60
        if unit in ["hour", "hours"]:
            return duration * 3600
        if unit in ["day", "days"]:
            return duration * 86400
        raise ValueError("Invalid time unit")

async def setup(client):
    await client.add_cog(Moderation(client))
