import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp as youtube_dl
import random
import os
import asyncio
from dotenv import load_dotenv

# Load the .env file for sensitive data (like your token)
load_dotenv()

# Get the Discord Token from .env file
TOKEN = os.getenv("DISCORD_TOKEN")

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

# Custom Help Command (Prefix !)
bot.remove_command("help")

@bot.command(name="help-bot", help="Displays this help message")
async def custom_help(ctx):
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

# custom polls 

@bot.tree.command(name="poll", description="Create a customizable poll with up to 10 options.")
async def slash_poll(interaction: discord.Interaction, question: str, *options: str):
    if len(options) < 2:
        await interaction.response.send_message("❌ **You need at least two options to create a poll!**", ephemeral=True)
        return
    if len(options) > 10:
        await interaction.response.send_message("❌ **You can provide up to 10 options only!**", ephemeral=True)
        return

    embed = discord.Embed(
        title="📊 **Poll Time!**",
        description=f"**{question}**\n\nVote by reacting below!",
        color=0x1abc9c
    )

    reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    for i, option in enumerate(options):
        embed.add_field(name=f"{reactions[i]} Option {i + 1}", value=option, inline=False)

    message = await interaction.response.send_message(embed=embed)
    poll_message = await interaction.original_response()

    for i in range(len(options)):
        await poll_message.add_reaction(reactions[i])

# server-info
@bot.tree.command(name="serverinfo", description="Displays detailed information about the server.")
async def slash_serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(
        title=f"🌟 Server Info for {guild.name}",
        color=0xf1c40f
    )
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    embed.add_field(name="👑 Owner", value=str(guild.owner), inline=True)
    embed.add_field(name="📅 Created On", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="👥 Members", value=f"{guild.member_count} members", inline=True)
    embed.add_field(name="💬 Channels", value=f"{len(guild.text_channels)} text / {len(guild.voice_channels)} voice", inline=True)
    embed.add_field(name="🛡️ Roles", value=f"{len(guild.roles)} roles", inline=True)
    embed.add_field(name="🌍 Region", value=str(guild.region), inline=True)
    embed.set_footer(text=f"Server ID: {guild.id}")
    await interaction.response.send_message(embed=embed)
# number game 
@bot.tree.command(name="guessnumber", description="Guess the number (1-100). Flashy version!")
async def slash_guessnumber(interaction: discord.Interaction):
    number = random.randint(1, 100)
    embed = discord.Embed(
        title="🔢 Guess the Number Game!",
        description="I have picked a number between **1** and **100**. Can you guess it?",
        color=0x9b59b6
    )
    embed.set_footer(text="Type your guess in chat!")
    await interaction.response.send_message(embed=embed)

    def check(m):
        return m.author == interaction.user

    try:
        while True:
            message = await bot.wait_for("message", timeout=30.0, check=check)
            guess = int(message.content)
            if guess < number:
                await interaction.channel.send("🔽 Higher!")
            elif guess > number:
                await interaction.channel.send("🔼 Lower!")
            else:
                await interaction.channel.send(f"🎉 Correct! The number was **{number}**. Great job, {interaction.user.mention}!")
                break
    except asyncio.TimeoutError:
        await interaction.followup.send(f"⏰ Time's up! The number was **{number}**.")
#fun facts 
@bot.tree.command(name="funfact", description="Get a random fun fact.")
async def slash_funfact(interaction: discord.Interaction):
    facts = [
        "🍯 **Did you know?** Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old!",
        "🐙 Octopuses have **three hearts** and **blue blood**!",
        "🌡️ The Eiffel Tower grows taller during summer. It can be up to **15 cm** taller due to the metal expanding in the heat.",
        "🍌 Bananas are berries, but strawberries are not. Mind blown yet? 🍓",
        "🦈 Sharks existed before trees and have been around for over **400 million years**.",
        "🐋 The heart of a blue whale weighs about **400 pounds** and can be heard beating from two miles away.",
        "🎵 **Music trivia:** Did you know Mozart wrote his first symphony at the age of **8**?",
        "💧 Antarctica is technically a desert, and it holds **70% of the world's freshwater**.",
        "🐾 A group of flamingos is called a 'flamboyance.' 🦩",
        "💻 The first computer bug was an actual **moth** found in a computer in 1947.",
        "🚀 Astronauts grow taller in space due to the lack of gravity compressing their spine!",
        "📚 The longest novel ever written is **'In Search of Lost Time'** by Marcel Proust, which contains over **1.2 million words**.",
        "🦖 Dinosaurs roamed the Earth for about **165 million years**, compared to humans' mere **200,000 years**.",
        "🎯 The chance of getting struck by lightning in your lifetime is approximately **1 in 15,300**.",
        "🌌 There are more stars in the universe than grains of sand on all the Earth's beaches. ⭐",
    ]
    fact = random.choice(facts)
    embed = discord.Embed(
        title="🌟 **Fun Fact!**",
        description=fact,
        color=0x57f287  # A bright, fun green
    )
    embed.set_footer(text="Learn something new every day! 💡")
    await interaction.response.send_message(embed=embed)
#jokes 
@bot.tree.command(name="joke", description="Get a random hilarious joke.")
async def slash_joke(interaction: discord.Interaction):
    jokes = [
        "😹 **Why don't skeletons fight each other?** Because they don't have the guts!",
        "🚴 **Why couldn't the bicycle stand up by itself?** It was two tired.",
        "🥚 **Why don't eggs tell jokes?** They'd crack each other up.",
        "🍝 **What do you call fake spaghetti?** An impasta!",
        "🌌 **How do you organize a space party?** You planet.",
        "🔬 **Why don't scientists trust atoms?** Because they make up everything!",
        "🌾 **Why did the scarecrow win an award?** Because he was outstanding in his field!",
        "🏌️ **Why did the golfer bring two pairs of pants?** In case he got a hole in one!",
        "😲 **I told my wife she was drawing her eyebrows too high.** She looked surprised.",
        "🐶 **Why do dogs run in circles?** Because it's hard to run in squares!",
        "👽 **Why did the alien go to school?** To improve his space grades.",
        "🎸 **Why did the musician go to jail?** Because he got caught playing a sharp!",
        "🧀 **What do you call cheese that isn't yours?** Nacho cheese!",
        "🦄 **Why don’t unicorns play hide and seek?** Because they are always a little horn-y.",
        "🐟 **Why are fish so smart?** Because they live in schools!",
        "🧛 **Why don’t vampires attack Taylor Swift?** Because she has bad blood.",
        "🎂 **Why did the cake go to the doctor?** It was feeling crumby!",
        "🐍 **Why don’t snakes drink coffee?** Because it makes them viperactive!",
        "🍕 **What’s a pizza’s favorite song?** Slice, slice baby!"
    ]
    joke = random.choice(jokes)
    embed = discord.Embed(
        title="🤣 **Here's a Joke for You!**",
        description=joke,
        color=0xf1c40f  # Bright yellow for humor
    )
    embed.set_footer(text="Laughter is the best medicine! 😂")
    await interaction.response.send_message(embed=embed)

# Run the bot
bot.run(TOKEN)
