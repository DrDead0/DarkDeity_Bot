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

# Additional commands
@bot.command(name="welcome", help="Sends a welcome message")
async def welcome(ctx):
    await ctx.send("Welcome to the server! Please make sure to read the rules and enjoy your time here!")

@bot.command(name="rules", help="Displays the server rules")
async def rules(ctx):
    rules_text = """
    1. Discord TOS & Community Guidelines - All users need to follow Discord's Terms of Service and Community Guidelines.
       Punishment - Ban

    2. Bot Rules - As a Community server, we will enforce Bot rules.
       Punishment - Ban

    3. Racism - Any racial slurs or racist behavior/comments are NOT accepted.
       Punishment - Warn/Mute/Ban

    4. Channel Appropriacy - Keep things in the right channels.
       Punishment - Mute/Warn

    5. NSFW - No NSFW content is allowed.
       Punishment - Warn/Ban

    6. Voice Rules - No ear raping or inappropriate music in voice chat.
       Punishment - Mute/Warn

    7. Spam - No spamming of text, images, or emojis.
       Punishment - Mute/Warn

    8. Begging - Begging is strictly prohibited.
       Punishment - Warn/Mute

    9. Advertisement - No advertisements outside of #self-advertise and Partnerships.
       Punishment - Warn/Mute

    10. Common Sense - Use common sense and respect others.
        Punishment - Depends
    """
    await ctx.send(f"Server Rules:\n{rules_text}")

@bot.command(name="echo", help="Repeats the message provided by the user.")
async def echo(ctx, *, message: str):
    await ctx.send(message)

@bot.command(name="hello", help="Greets the user.")
async def hello(ctx):
    await ctx.send("Hello there! How can I assist you today?")

@bot.command(name="support", help="Provides the support server link.")
async def support(ctx):
    await ctx.send("For support, please join our [Support Server](your-support-server-link).")

@bot.command(name="contact", help="Provides contact information.")
async def contact(ctx):
    await ctx.send("You can contact us at: support@yourdomain.com")

@bot.command(name="ping", help="Checks the bot's latency.")
async def ping(ctx):
    await ctx.send(f"Pong! Latency is {round(bot.latency * 1000)}ms")

@bot.command(name="clear", help="Clears the specified number of messages.")
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"Cleared {amount} messages.", delete_after=5)

@bot.command(name="kick", help="Kicks a user from the server.")
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.User, *, reason: str = "No reason provided"):
    await user.kick(reason=reason)
    await ctx.send(f"Kicked {user.name} for reason: {reason}")

@bot.command(name="ban", help="Bans a user from the server.")
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.User, *, reason: str = "No reason provided"):
    await user.ban(reason=reason)
    await ctx.send(f"Banned {user.name} for reason: {reason}")

@bot.command(name="unban", help="Unbans a user from the server.")
@commands.has_permissions(ban_members=True)
async def unban(ctx, user: discord.User):
    await ctx.guild.unban(user)
    await ctx.send(f"Unbanned {user.name}")

# Music control commands
@bot.command(name="resume", help="Resumes the current music")
async def resume(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await ctx.send("Resumed the music.")
    else:
        await ctx.send("No music is paused.")

@bot.command(name="queue", help="Shows the music queue")
async def queue(ctx):
    # You can implement a queue system later if desired
    await ctx.send("This feature is under development.")

@bot.command(name="volume", help="Sets the music volume (0-100)")
async def volume(ctx, level: int):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client:
        if 0 <= level <= 100:
            voice_client.source.volume = level / 100
            await ctx.send(f"Volume set to {level}%")
        else:
            await ctx.send("Please provide a volume level between 0 and 100.")
    else:
        await ctx.send("Not currently playing any music.")

@bot.command(name="join", help="Makes the bot join the voice channel")
async def join(ctx):
    voice_channel = ctx.author.voice.channel
    await voice_channel.connect()
    await ctx.send(f"Joined {voice_channel.name}!")

@bot.command(name="leave", help="Makes the bot leave the voice channel")
async def leave(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client:
        await voice_client.disconnect()
        await ctx.send("Disconnected from the voice channel.")
    else:
        await ctx.send("I'm not connected to any voice channel.")

bot.run("YOUR_BOT_TOKEN")
