import discord
from discord.ext import commands
from time import time
import random
import os
from collections import defaultdict
from random import shuffle
import json
from discord import Member
from discord.ext.commands import has_permissions
import asyncio
import re
from discord.utils import get
import requests
from discord import TextChannel
from datetime import datetime
from discord.ext.commands import has_permissions as has_perms
from flask import Flask
import requests
import yt_dlp as youtube_dl
import subprocess
import yt_dlp

#intends and prefix commands .....................................
intents = discord.Intents.all()
client=commands.Bot(command_prefix ='&',intents=intents)
intents.message_content = True

#administrator.........................................................
@client.event
async def on_ready():
    print("Bot is ready.")
    activity=discord.Game("&help")
    await client.change_presence(status=discord.Status.online,activity=activity)
    for guild in client.guilds:
        await ensure_administrator_role(guild)
        
async def ensure_administrator_role(guild):
    administrator_role = discord.utils.get(guild.roles, name="Administrator")
    if not administrator_role:
        administrator_role = await guild.create_role(name="Administrator")
    
    if administrator_role not in guild.me.roles:
        
        await guild.me.add_roles(administrator_role)
        
# Unknown Commands..............................................
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ Command not found! Use `&help` to see the available ones.")
    else:
        raise error

async def disconnect_after(ctx, delay=60):
    await asyncio.sleep(delay)
    if ctx.voice_client and not ctx.voice_client.is_playing():
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Left the voice channel due to inactivity.")

#status command .................................................
@client.command()
async def status(ctx):
    await ctx.send("Basic Commands : ✅\n"
                   "Moderation Commands : ✅\n "
                   "Game Commands : ✅\n"
                   "Music Commands : ✅\n"
                   "AI Chatbot : ❌\n")

#ping command............................................
@client.command()
async def ping(ctx):
    if round(client.latency * 1000) <= 50:
        embed=discord.Embed(title="PING", description=f"The ping is **{round(client.latency *1000)}** milliseconds!", color=0x44ff44)
    elif round(client.latency * 1000) <= 100:
        embed=discord.Embed(title="PING", description=f"The ping is **{round(client.latency *1000)}** milliseconds!", color=0xffd000)
    elif round(client.latency * 1000) <= 200:
        embed=discord.Embed(title="PING", description=f"The ping is **{round(client.latency *1000)}** milliseconds!", color=0xff6600)
    else:
        embed=discord.Embed(title="PING", description=f"The ping is **{round(client.latency *1000)}** milliseconds!", color=0x990000)
    await ctx.send(embed=embed)

#show commands command ............................................   
client.remove_command("help")
@client.command()
async def help(ctx):

    music_commands =[
        ("join" , "Joins to the VC joined by the user. Syntax: `&join`"),
        ("play" , "Joins to the VC and plays the searched song. Syntax: `&play [song_name]`"),
        ("pause" , "Pause the current song. Syntax: `&pause`"),
        ("resume" , "Resume the recently paused song. Syntax: `&resume`"),
        ("stop" , "Stops the currently playing song . Syntax: `&stop`"),
        ("skip" , "Skips the current playing song. Syntax: `&skip`"),
        ("queue" , "Shows the queue of the song. Syntax: `&queue`")
    ]

    moderation_commands = [
        ("setroles", "Sets roles allowed for commands. Syntax: `&setroles [cmd] [role]`"),
        ("kick", "Kicks a member. Syntax: `&kick [member] [reason]`"),
        ("ban", "Bans a member. Syntax: `&ban [member] [reason]`"),
        ("mute", "Mutes a member. Syntax: `&mute @member <duration> <time_unit> <reason>`"),
        ("unmute", "Unmutes a member. Syntax: `&unmute [member]`"),
        ("addrole", "Adds a role. Syntax: `&addrole [member] [role]`"),
        ("removerole", "Removes a role. Syntax: `&removerole [member] [role]`"),
        ("add_banned_word", "Adds a banned word. Syntax: `&add_banned_word [word]`"),
        ("remove_banned_word", "Removes a banned word. Syntax: `&remove_banned_word [word]`")
    ]

    game_commands = [
        ("truth", "Random truth. Syntax: `&truth`"),
        ("dare", "Random dare. Syntax: `&dare`")
    ]

    general_commands = [
        ("status", "Shows bot status. Syntax: `&status`"),
        ("ping", "Shows ping. Syntax: `&ping`"),
        ("time", "Shows time. Syntax: `&time`"),
        ("owner", "Shows bot owner and info. Syntax: `&owner`"),
        ("suggest", "Gives suggestion form. Syntax: `&suggest`")
    ]

    embed = discord.Embed(
        title="🤖 Bot Command List",
        description="Here are all my available commands, grouped by category:",
        color=discord.Color.teal()
    )

    embed.set_thumbnail(url=client.user.avatar.url if client.user.avatar else None)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
    
    embed.add_field(
        name="🎵 Music Commands",
        value="\n".join(f"**`&{cmd}`** — {desc}" for cmd, desc in music_commands),
        inline=False
    )
    # Moderation Commands....................................................
    embed.add_field(
        name="⚙️ Moderation Commands",
        value="\n".join(f"**`&{cmd}`** — {desc}" for cmd, desc in moderation_commands),
        inline=False
    )

    # Game Commands...........................................................
    embed.add_field(
        name="🎮 Game Commands",
        value="\n".join(f"**`&{cmd}`** — {desc}" for cmd, desc in game_commands),
        inline=False
    )

    # General Commands.........................................................
    embed.add_field(
        name="ℹ️ General Commands",
        value="\n".join(f"**`&{cmd}`** — {desc}" for cmd, desc in general_commands),
        inline=False
    )

    await ctx.send(embed=embed)


#time command .......................................................
@client.command()
async def time(ctx):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    await ctx.send(f'The current time is: {current_time}')

#owners command ...................................................
@client.command()
async def owner(ctx):
    await ctx.send(f"Good day to you {ctx.author.mention}. My name is Kartik and I got an glorious opportunity to build this bot. This initiative was "
                    "starting back in 2021 as a basic truth and dare bot but now with new technologies evolving , I thought to take this onto a new level using and trying to use AI and ML in the bot "
                    "Please check the status for more info about the bot.")     

#Truth game .................................................(Upgrade it on a daily basis)
@client.command(pass_context=True)
async def truth(ctx):
    a="Do you have a girlfriend?"
    b="Who was your first kiss?"
    c="Who do you have crush on?"
    d="What's the most embarrassing moment of your life?"
    e="What's your favourite sport?"
    f="When was the last time you cried?"
    g="What's your biggest fear? (not philosophical)"
    h="Your best ever pickup line?"
    i="Who is your comfort character?"
    j="What's your weirdest fantasy?"
    l1=[a,b,c,d,e,f,g,h,i,j]
    shuffle(l1)
    embed=discord.Embed(title="TRUTH" , description=l1[0],color=0x44ff44)
    await ctx.send(embed=embed)

#Dare game.............................................................(Upgrade it on a daily basis)
@client.command(pass_context=True)
async def dare(ctx):
    a="Dance with your underwear in your hand"
    b="Sing a song on the top of your lungs from your window"
    c="Put on a frock on your neck and dance on Hotel California"
    d="Call a random number and talk like you are their previous reincarnation's partner"
    e="Show your weirdest photo available"
    f="Jump on your bed thrice and shout MarcoPolo"
    g="Speak out your will as if your funeral is tomorrow"
    h="Put your craziest clip online"
    i="Kiss an item from your room (tongue involved)"
    j="Balance a steel utensil on your nose and walk around for 30 seconds."
    l2=[a,b,c,d,e,f,g,h,i,j]
    shuffle(l2)
    embed=discord.Embed(title="DARE" , description=l2[0],color=0x44ff44)
    await ctx.send(embed=embed)
    
#Google Form......................................................(Suggestions Basically) 
@client.command()
async def suggest(ctx):
   google_form_link=''
   await ctx.send("Please fill out the suggestion form here: https://forms.gle/3t1G1gD6ZY8QPMrc9")

# For moderation.................................................
allowed_roles = {
    "kick": {},
    "ban": {},
    "mute": {},
    "addrole": {},
    "removerole": {},
    "unmute": {}
}

def has_allowed_role(ctx, command):
    creator_role = ctx.guild.owner
    allowed = allowed_roles.get(command, [])
    return ctx.author == creator_role or any(role.id in allowed for role in ctx.author.roles)

# Set roles command.........................................................
@client.command()
async def setroles(ctx, command: str, role: discord.Role, *roles_to_add: discord.Role):
    if ctx.author != ctx.guild.owner:
        await ctx.send("Only the server owner can use this command.")
        return

    command = command.lower()
    if command not in allowed_roles:
        await ctx.send("Invalid command. Please choose from 'kick', 'ban', 'mute', 'addrole', 'removerole', or 'unmute'.")
        return

    allowed_roles[command][role.name] = [r.id for r in roles_to_add]
    await ctx.send(f"Roles allowed to use {command} command have been set to: {', '.join(role.name for role in roles_to_add)}")

# Kick command..............................................................
@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if not has_allowed_role(ctx, "kick"):
        await ctx.send("You don't have permission to use this command.")
        return

    if reason is None:
        await ctx.send("Please provide a reason for kicking the member.")
        return

    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} has been kicked from the server. Reason: {reason}")

# Ban command.................................................................
@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if not has_allowed_role(ctx, "ban"):
        await ctx.send("You don't have permission to use this command.")
        return

    if reason is None:
        await ctx.send("Please provide a reason for banning the member.")
        return

    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been banned from the server. Reason: {reason}")

# Mute command........................................................
@client.command()
async def mute(ctx, member: discord.Member, duration: int = None, time_unit: str = None, *, reason=None):
    if not has_allowed_role(ctx, "mute"):
        await ctx.send("❌ You don't have permission to use this command.")
        return

    if duration is None or time_unit is None:
        await ctx.send("⚠️ Usage: `&mute @member <duration> <time_unit> <reason>`\nExample: `&mute @user 10 minutes spamming`")
        return

    if reason is None:
        await ctx.send("⚠️ Please provide a reason for muting the member.")
        return

    # Find or create Muted role...................................................
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not mute_role:
        try:
            mute_role = await ctx.guild.create_role(name="Muted", reason="To mute users")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False)
        except discord.Forbidden:
            await ctx.send("❌ I don't have the permissions to create roles.")
            return

    # Apply mute...................................................................
    await member.add_roles(mute_role)
    await ctx.send(f"🔇 {member.mention} has been muted for {duration} {time_unit}. Reason: {reason}")

    # Schedule unmute..............................................................
    try:
        await asyncio.sleep(convert_to_seconds(duration, time_unit))
    except ValueError:
        await ctx.send("⚠️ Invalid time unit. Please use `seconds`, `minutes`, `hours`, or `days`.")
        return

    await member.remove_roles(mute_role)
    await ctx.send(f"✅ {member.mention} has been unmuted after {duration} {time_unit}.")


def convert_to_seconds(duration, time_unit):
    if time_unit.lower() in ["second", "seconds"]:
        return duration
    elif time_unit.lower() in ["minute", "minutes"]:
        return duration * 60
    elif time_unit.lower() in ["hour", "hours"]:
        return duration * 3600
    elif time_unit.lower() in ["day", "days"]:
        return duration * 86400
    else:
        raise ValueError("Invalid time unit")

        
# Unmute command.........................................................................
@client.command()
async def unmute(ctx, member: discord.Member):
    if not has_allowed_role(ctx, "unmute"):
        await ctx.send("You don't have permission to use this command.")
        return

    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not mute_role:
        await ctx.send("Mute role not found.")
        return

    if mute_role in member.roles:
        await member.remove_roles(mute_role)
        await ctx.send(f"{member.mention} has been unmuted.")
    else:
        await ctx.send(f"{member.mention} is not muted.") 

# Add role command.......................................................................
@client.command()
async def addrole(ctx, member: discord.Member, role: discord.Role):
    if not has_allowed_role(ctx, "addrole"):
        await ctx.send("You don't have permission to use this command.")
        return

    await member.add_roles(role)
    await ctx.send(f"Added role '{role.name}' to {member.mention}.")

# Remove role command....................................................................
@client.command()
async def removerole(ctx, member: discord.Member, role: discord.Role):
    if not has_allowed_role(ctx, "removerole"):
        await ctx.send("You don't have permission to use this command.")
        return

    await member.remove_roles(role)
    await ctx.send(f"Removed role '{role.name}' from {member.mention}.")

def load_banned_words():
    try:
        with open("banned_words.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_banned_words(banned_words):
    with open("banned_words.json", "w") as file:
        json.dump(banned_words, file)

banned_words_per_guild = load_banned_words()

def contains_banned_word(message_content, guild_id):
    banned_words = banned_words_per_guild.get(str(guild_id), [])
    for word in banned_words:
        if re.search(r'\b' + re.escape(word) + r'\b', message_content, re.IGNORECASE):
            return True
    return False

@client.command()
async def add_banned_word(ctx, word):
    if ctx.author.guild_permissions.administrator:
        guild_id = ctx.guild.id
        if str(guild_id) not in banned_words_per_guild:
            banned_words_per_guild[str(guild_id)] = []
        banned_words_per_guild[str(guild_id)].append(word.lower())
        save_banned_words(banned_words_per_guild)
        await ctx.send(f"'{word}' has been added to the banned words list.")
    else:
        await ctx.send("You don't have permission to use this command.")

@client.command()
async def remove_banned_word(ctx, word):
    if ctx.author.guild_permissions.administrator:
        guild_id = ctx.guild.id
        banned_words = banned_words_per_guild.get(str(guild_id), [])
        if word.lower() in banned_words:
            banned_words.remove(word.lower())
            banned_words_per_guild[str(guild_id)] = banned_words
            save_banned_words(banned_words_per_guild)
            await ctx.send(f"'{word}' has been removed from the banned words list.")
        else:
            await ctx.send(f"'{word}' is not in the banned words list.")
    else:
        await ctx.send("You don't have permission to use this command.")

@client.event
async def on_disconnect():
    save_banned_words(banned_words_per_guild)

WARNINGS_FILE = "warnings.json"

# Load warnings from file......................................................................
def load_warnings():
    if os.path.exists(WARNINGS_FILE):
        with open(WARNINGS_FILE, "r") as f:
            return json.load(f)
    return {}

# Save warnings to file...........................................................................
def save_warnings(data):
    with open(WARNINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

warnings = load_warnings()  

def add_warning(guild_id, user_id):
    guild_id = str(guild_id)
    user_id = str(user_id)

    if guild_id not in warnings:
        warnings[guild_id] = {}
    if user_id not in warnings[guild_id]:
        warnings[guild_id][user_id] = 0

    warnings[guild_id][user_id] += 1
    save_warnings(warnings)

    return warnings[guild_id][user_id]

def reset_warnings(guild_id, user_id):
    guild_id = str(guild_id)
    user_id = str(user_id)
    if guild_id in warnings and user_id in warnings[guild_id]:
        warnings[guild_id][user_id] = 0
        save_warnings(warnings)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    guild_id = message.guild.id
    user_id = message.author.id

    if contains_banned_word(message.content, guild_id):
        await message.delete()

        warning_count = add_warning(guild_id, user_id)

        if warning_count < 5:
            await message.channel.send(
                f"{message.author.mention} ⚠️ Warning {warning_count}/5: Watch your language!"
            )
        else:
            reset_warnings(guild_id, user_id) 

            mute_role = discord.utils.get(message.guild.roles, name="Muted")
            if not mute_role:
                try:
                    mute_role = await message.guild.create_role(
                        name="Muted", reason="Auto mute for bad language"
                    )
                    for channel in message.guild.channels:
                        await channel.set_permissions(mute_role, send_messages=False)
                except discord.Forbidden:
                    await message.channel.send("❌ I don’t have permission to create/manage roles.")
                    return

            await message.author.add_roles(mute_role)
            await message.channel.send(
                f"🔇 {message.author.mention} has been muted for 1 day due to repeated violations."
            )

            await asyncio.sleep(86400)  
            await message.author.remove_roles(mute_role)
            await message.channel.send(
                f"✅ {message.author.mention} has been unmuted after serving their 1-day mute."
            )

    await client.process_commands(message)

class MusicPlayer:
    def __init__(self, ctx):
        self.ctx = ctx
        self.voice = None
        self.queue = []
        self.is_playing = False

    async def play_next(self, error=None):
        if error:
            print(f"Error: {error}")
        if len(self.queue) > 0:
            next_query = self.queue.pop(0)
            await self.play_song(next_query)  # Only play from queue
        else:
            self.is_playing = False
            if self.voice and self.voice.is_connected():
                await asyncio.sleep(10)
                if not self.is_playing and len(self.queue) == 0:
                    await self.voice.disconnect()

    async def play_song(self, query):
        """Search YouTube and play the first matching result"""
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'default_search': 'ytsearch1',  # Search instead of URL
        }

        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                if 'entries' in info:  # if it’s a search
                    info = info['entries'][0]
                audio_url = info['url']
                title = info.get('title', 'Unknown Title')

            source = discord.FFmpegPCMAudio(audio_url, **ffmpeg_options)
            self.voice.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(e), client.loop))
            self.is_playing = True
            await self.ctx.send(f"🎶 Now playing: **{title}**")

        except Exception as e:
            await self.ctx.send(f"⚠️ Error playing audio: {e}")
            print(e)


# Store MusicPlayer objects per guild
client.voice_players = {}  

# ---------------------- COMMANDS ----------------------
@client.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_connected():
            await voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"🟢 Joined `{channel}`")
    else:
        await ctx.send("❌ You must be in a voice channel first!")

@client.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Left the voice channel.")
    else:
        await ctx.send("❌ I'm not in a voice channel!")

@client.command()
async def play(ctx, *, query: str):
    guild_id = ctx.guild.id
    if guild_id not in client.voice_players:
        client.voice_players[guild_id] = MusicPlayer(ctx)

    player = client.voice_players[guild_id]

    # Connect if not connected
    if ctx.voice_client is None:
        if ctx.author.voice:
            player.voice = await ctx.author.voice.channel.connect()
        else:
            await ctx.send("❌ You need to join a voice channel first!")
            return
    else:
        player.voice = ctx.voice_client

    # Append to queue
    player.queue.append(query)
    await ctx.send(f"✅ Added to queue: **{query}**")

    # Play only if nothing is currently playing
    if not player.is_playing:
        next_query = player.queue.pop(0)  # Remove from queue and play
        await player.play_song(next_query)

@client.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭️ Skipped current song.")
    else:
        await ctx.send("❌ Nothing to skip.")

@client.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸️ Paused playback.")
    else:
        await ctx.send("❌ Nothing is playing to pause.")

@client.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶️ Resumed playback.")
    else:
        await ctx.send("❌ Nothing is paused.")

@client.command()
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("⏹️ Stopped playback.")
    else:
        await ctx.send("❌ Nothing to stop.")

@client.command()
async def queue(ctx):
    guild_id = ctx.guild.id
    if guild_id not in client.voice_players or len(client.voice_players[guild_id].queue) == 0:
        await ctx.send("🎵 The queue is empty.")
        return

    player = client.voice_players[guild_id]
    queue_list = player.queue

    message = "🎶 **Upcoming Songs:**\n"
    for i, song in enumerate(queue_list, start=1):
        message += f"{i}. {song}\n"
    await ctx.send(message)
    
client.run("")  #Important(Ask Me)(Gets Expired if uploaded online so) 
