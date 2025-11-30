import discord
from discord.ext import commands
import yt_dlp
import asyncio
import json
import os

PLAYLIST_FILE = "data/playlists.json"

def load_playlists():
    if os.path.exists(PLAYLIST_FILE):
        with open(PLAYLIST_FILE, "r") as f:
            return json.load(f)
    return {}


def save_playlists(data):
    os.makedirs("data", exist_ok=True)
    with open(PLAYLIST_FILE, "w") as f:
        json.dump(data, f, indent=4)


playlists = load_playlists()


class MusicPlayer:
    def __init__(self, ctx):
        self.ctx = ctx
        self.voice = None
        self.queue = []
        self.is_playing = False

    # ------------------------ PLAY NEXT --------------------------
    async def play_next(self, error=None):
        if error:
            print("Music error:", error)

        if len(self.queue) > 0:
            next_query, requester = self.queue.pop(0)
            await self.play_song(next_query)
        else:
            self.is_playing = False
            await asyncio.sleep(10)
            if not self.is_playing:
                if self.voice and self.voice.is_connected():
                    await self.voice.disconnect()

#PLAY SONG 

    async def play_song(self, query):
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'default_search': 'ytsearch1'
        }

        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                if 'entries' in info:
                    info = info['entries'][0]

            audio_url = info['url']
            title = info.get('title', 'Unknown Title')

            source = discord.FFmpegPCMAudio(audio_url, **ffmpeg_options)

            self.voice.play(
                source,
                after=lambda e: asyncio.run_coroutine_threadsafe(
                    self.play_next(e), self.ctx.bot.loop
                )
            )

            self.is_playing = True
            await self.ctx.send(f"🎵 Now playing: **{title}**")

        except Exception as e:
            await self.ctx.send(f"⚠️ Error: {e}")
            print("Music error:", e)

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.voice_players = {}  # guild_id → MusicPlayer

#PLAYLIST UTILITIES (HELPER FUNCTIONS)

    def get_user_playlist(self, guild_id, user_id):
        gid, uid = str(guild_id), str(user_id)

        if gid not in playlists:
            playlists[gid] = {}

        if uid not in playlists[gid]:
            playlists[gid][uid] = {"songs": []}

        return playlists[gid][uid]

#PLAYLIST COMMANDS

    @commands.command()
    async def create_playlist(self, ctx):
        gid = str(ctx.guild.id)
        uid = str(ctx.author.id)

        if gid in playlists and uid in playlists[gid]:
            return await ctx.send("❌ You already have a playlist!")

        playlists.setdefault(gid, {})[uid] = {"songs": []}
        save_playlists(playlists)

        await ctx.send("🎵 Your playlist has been created!")

    @commands.command()
    async def delete_playlist(self, ctx):
        gid = str(ctx.guild.id)
        uid = str(ctx.author.id)

        if gid in playlists and uid in playlists[gid]:
            del playlists[gid][uid]
            save_playlists(playlists)
            return await ctx.send("🗑️ Your playlist has been deleted.")

        await ctx.send("❌ You don't have a playlist to delete.")

    @commands.command()
    async def add_to_playlist(self, ctx, *, song):
        data = self.get_user_playlist(ctx.guild.id, ctx.author.id)
        data["songs"].append(song)

        save_playlists(playlists)

        await ctx.send(f"➕ Added **{song}** to your playlist.")

    @commands.command()
    async def show_playlist(self, ctx):
        data = self.get_user_playlist(ctx.guild.id, ctx.author.id)

        if not data["songs"]:
            return await ctx.send("📭 Your playlist is empty.")

        msg = "🎶 **Your Playlist:**\n"
        for i, song in enumerate(data["songs"], start=1):
            msg += f"{i}. {song}\n"

        await ctx.send(msg)

#PLAY PLAYLIST (WITH POSITION)

    @commands.command()
    async def play_playlist(self, ctx, start_pos: int = 1):
        data = self.get_user_playlist(ctx.guild.id, ctx.author.id)

        if not data["songs"]:
            return await ctx.send("❌ Your playlist is empty.")

        songs = data["songs"]

        if start_pos < 1 or start_pos > len(songs):
            return await ctx.send("❌ Invalid starting position.")

        # Play from start_pos → end
        for i in range(start_pos - 1, len(songs)):
            await ctx.invoke(self.client.get_command("play"), query=songs[i])

        await ctx.send(f"🎧 Playing your playlist from position **{start_pos}**…" )


#MUSIC COMMANDS

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

            if voice_client and voice_client.is_connected():
                await voice_client.move_to(channel)
            else:
                await channel.connect()

            await ctx.send(f"🟢 Joined `{channel}`")
        else:
            await ctx.send("❌ You must join a voice channel first!")

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("👋 Disconnected.")
        else:
            await ctx.send("❌ I'm not in a voice channel.")

    @commands.command()
    async def play(self, ctx, *, query: str):
        guild_id = ctx.guild.id

        if guild_id not in self.client.voice_players:
            self.client.voice_players[guild_id] = MusicPlayer(ctx)

        player = self.client.voice_players[guild_id]

        if ctx.voice_client is None:
            if ctx.author.voice:
                player.voice = await ctx.author.voice.channel.connect()
            else:
                return await ctx.send("❌ Join a voice channel first!")
        else:
            player.voice = ctx.voice_client

        player.queue.append((query, ctx.author.name))
        await ctx.send(f"➕ Added to queue: **{query}**")

        if not player.is_playing:
            next_query, requester = player.queue.pop(0)
            await player.play_song(next_query)

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏭️ Skipped.")
        else:
            await ctx.send("❌ Nothing to skip.")

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ Paused.")
        else:
            await ctx.send("❌ Nothing is playing.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Resumed.")
        else:
            await ctx.send("❌ Nothing is paused.")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.send("⏹️ Stopped.")
        else:
            await ctx.send("❌ Not playing anything.")

    @commands.command()
    async def queue(self, ctx):
        guild_id = ctx.guild.id

        if guild_id not in self.client.voice_players:
            return await ctx.send("🎵 Queue is empty.")

        player = self.client.voice_players[guild_id]

        if len(player.queue) == 0:
            return await ctx.send("🎵 Queue is empty.")

        msg = "🎶 **Upcoming Songs:**\n"
        for i, (song, user) in enumerate(player.queue, start=1):
            msg += f"{i}. {song} *(Requested by {user})*\n"

        await ctx.send(msg)

async def setup(client):
    await client.add_cog(Music(client))
    