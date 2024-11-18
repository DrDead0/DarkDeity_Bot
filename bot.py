import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import random
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Music setup
ytdl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegAudioConvertor',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

ffmpeg_opts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

# Bot Event for Ready State
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    print("------")

# Music commands
@bot.command(name="play", help="Plays music from a YouTube URL")
async def play(ctx, url: str):
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()

    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio(url2, **ffmpeg_opts))

    await ctx.send(f"Now playing: {info['title']}")

@bot.command(name="pause", help="Pauses the current music")
async def pause(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Paused the music.")
    else:
        await ctx.send("No music is playing.")

@bot.command(name="skip", help="Skips the current song")
async def skip(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Skipping the song.")
    else:
        await ctx.send("No music is playing.")

@bot.command(name="stop", help="Stops the music and disconnects the bot")
async def stop(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client:
        await voice_client.disconnect()
        await ctx.send("Disconnected and stopped the music.")
    else:
        await ctx.send("I'm not connected to any voice channel.")

# Fun Commands
@bot.command(name="coinflip", help="Flips a coin")
async def coinflip(ctx):
    outcome = random.choice(["Heads", "Tails"])
    await ctx.send(f"The coin landed on: {outcome}")

@bot.command(name="roll", help="Rolls a dice with specified sides (e.g., !roll 20)")
async def roll(ctx, sides: int):
    result = random.randint(1, sides)
    await ctx.send(f"You rolled: {result}")

@bot.command(name="userinfo", help="Displays information about a user")
async def userinfo(ctx, user: discord.User):
    embed = discord.Embed(title=f"User Info - {user.name}", color=0x3498db)
    embed.add_field(name="ID", value=user.id)
    embed.add_field(name="Created At", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    embed.add_field(name="Joined At", value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S"))
    await ctx.send(embed=embed)

# Server info
@bot.command(name="info", help="Displays information about the server")
async def info(ctx):
    embed = discord.Embed(title=f"Server Info - {ctx.guild.name}", color=0x3498db)
    embed.add_field(name="Server ID", value=ctx.guild.id)
    embed.add_field(name="Created At", value=ctx.guild.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    embed.add_field(name="Members", value=ctx.guild.member_count)
    await ctx.send(embed=embed)

# Help command
@bot.command(name="help", help="Displays this help message")
async def help(ctx):
    embed = discord.Embed(title="Help Menu", description="Available Commands", color=0x3498db)
    embed.add_field(name="!play <url>", value="Plays music from a YouTube URL.")
    embed.add_field(name="!pause", value="Pauses the current music.")
    embed.add_field(name="!skip", value="Skips the current song.")
    embed.add_field(name="!coinflip", value="Flips a coin (Heads or Tails).")
    embed.add_field(name="!roll <sides>", value="Rolls a dice with the specified number of sides.")
    embed.add_field(name="!userinfo <user>", value="Displays information about a user.")
    embed.add_field(name="!info", value="Displays information about the server.")
    await ctx.send(embed=embed)

# Run the bot
bot.run(os.getenv("DISCORD_TOKEN"))
