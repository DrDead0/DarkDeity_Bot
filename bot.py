import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp as youtube_dl
import random
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Required for member join events

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

# Bot Event for Member Join
@bot.event
async def on_member_join(member):
    # Welcome message in the server
    welcome_channel = discord.utils.get(member.guild.text_channels, name="general")  # Customize the channel
    if welcome_channel:
        await welcome_channel.send(f"🎉 Welcome to the server, {member.mention}! 🎉\nPlease make sure to read the rules and enjoy your time here! 👾")

    # Send rules via DM
    try:
        dm_message = """
        🎉 **Welcome to the Server!** 🎉

        Please take a moment to read the rules carefully:

        1️⃣ **Discord TOS & Community Guidelines**  
        All users need to follow Discord's Terms of Service and Community Guidelines.  
        **Punishment** - Ban

        2️⃣ **Bot Rules**  
        As a Community server, we will enforce Bot rules.  
        **Punishment** - Ban

        3️⃣ **Racism**  
        Any racial slurs or racist behavior/comments are NOT accepted in this server.  
        **Punishment** - Warn/Mute/Ban

        4️⃣ **Channel Appropriacy**  
        Please try to keep things in the right channels!  
        **Punishment** - Mute/Warn

        5️⃣ **NSFW**  
        NSFW content is against the rules. This includes gore, porn, and violent videos/images. It also includes conversations about sensitive and inappropriate topics.  
        **Punishment** - Warn/Ban

        6️⃣ **Voice Rules**  
        Ear raping, playing unreasonable sounds through a mic, or putting on inappropriate music goes against our rules. Voice chat hopping is also not allowed.  
        **Punishment** - Mute/Warn

        7️⃣ **Spam**  
        Spamming text, images, or emojis is not allowed. If you spam, you will most likely be muted by auto-moderation bots.  
        **Punishment** - Mute/Warn

        8️⃣ **Begging**  
        Begging is strictly prohibited in this server. This also includes bot currency/nitro.  
        **Punishment** - Warn/Mute

        9️⃣ **Advertisement**  
        Advertisements of any kind are not allowed in this server outside of #self-advertise and Partnerships.  
        **Punishment** - Warn/Mute

        🔟 **Common Sense**  
        Since we can't include everything in a short set of rules, but using your common sense is really important. Exploiting loopholes in our rules is not allowed.  
        **Punishment** - Depends

        📌 **Don't forget to check pinned messages and channel descriptions for channel-specific rules!**
        """
        await member.send(dm_message)
    except discord.Forbidden:
        print(f"Couldn't send DM to {member.name}. They may have DMs disabled.")

# Bot Event for Member Leave
@bot.event
async def on_member_remove(member):
    # Send goodbye DM
    try:
        dm_message = f"""
        😢 Sorry to see you go, {member.name}! 😢

        Thank you for being part of our community. We hope you enjoyed your time here.  
        If you ever want to come back, you are always welcome! Feel free to join us again anytime.  

        Here's the link to rejoin the server: [Join Here](YOUR_SERVER_INVITE_LINK)
        """
        await member.send(dm_message)
    except discord.Forbidden:
        print(f"Couldn't send DM to {member.name}. They may have DMs disabled.")

# Music Commands (Prefix !)
@bot.command(name="play", help="Plays music from a YouTube URL")
async def play(ctx, url: str):
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()

    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio(url2, **ffmpeg_opts))

    await ctx.send(f"Now playing: {info['title']}")

# Moderation Commands (Prefix !)
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

# Slash Commands (Prefix /)
@bot.tree.command(name="play", description="Plays music from a YouTube URL")
async def slash_play(interaction: discord.Interaction, url: str):
    voice_channel = interaction.user.voice.channel
    voice_client = await voice_channel.connect()

    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio(url2, **ffmpeg_opts))

    await interaction.response.send_message(f"Now playing: {info['title']}")

@bot.tree.command(name="coinflip", description="Flips a coin (Heads or Tails).")
async def slash_coinflip(interaction: discord.Interaction):
    result = random.choice(["Heads", "Tails"])
    await interaction.response.send_message(f"The coin landed on: {result}")

@bot.tree.command(name="userinfo", description="Displays information about a user.")
async def slash_userinfo(interaction: discord.Interaction, user: discord.User):
    embed = discord.Embed(title=f"{user.name}'s Info", color=0x3498db)
    embed.add_field(name="ID", value=user.id)
    embed.add_field(name="Created at", value=user.created_at)
    embed.add_field(name="Joined at", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar.url)
    await interaction.response.send_message(embed=embed)

# Help Command (Prefix !)
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
    embed.add_field(name="!welcome", value="Sends a welcome message.")
    embed.add_field(name="!rules", value="Displays the server rules.")
    await ctx.send(embed=embed)

# Run the bot
bot.run("YOUR_BOT_TOKEN")
