import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve bot token from .env
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Intents for the bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_members = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')  # Remove default help command

# Event: Bot ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")

# Event: On member join (welcome message)
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='welcome')
    if channel:
        await channel.send(f"Welcome to the server, {member.mention}! 🎉")

# Command: Welcome message
@bot.command(name="welcome", description="Sends a welcome message to the designated channel.")
async def welcome(ctx):
    await ctx.send("Welcome to the server! Please read the rules and have fun! 🎉")

# Command: Rules
@bot.command(name="rules", description="Posts the server rules.")
async def rules(ctx):
    await ctx.send("""
**Server Rules**:
1. Be respectful to others.
2. No spamming or self-promotion.
3. Follow Discord's Terms of Service.
4. Have fun!
    """)

# Command: Help
@bot.command(name="help", description="Displays the help message with a list of available commands.")
async def help(ctx):
    embed = discord.Embed(
        title="DarkDeity Help Menu",
        description="Here is a list of available commands:",
        color=0x00ff00
    )
    embed.add_field(name="!welcome", value="Sends a welcome message.", inline=False)
    embed.add_field(name="!rules", value="Posts the server rules.", inline=False)
    embed.add_field(name="!echo [message]", value="Repeats the message back to the channel.", inline=False)
    embed.add_field(name="!hello", value="Greets the user.", inline=False)
    embed.add_field(name="!support", value="Raise a ticket for bot issues.", inline=False)
    embed.add_field(name="!contact", value="Displays contact information for the server admin.", inline=False)
    embed.add_field(name="!info", value="Provides information about the server.", inline=False)
    embed.add_field(name="!ping", value="Checks the bot's response time to Discord.", inline=False)
    embed.add_field(name="!clear [number]", value="Deletes a specified number of messages from a channel.", inline=False)
    await ctx.send(embed=embed)

# Command: Echo
@bot.command(name="echo", description="Repeats the message back to the channel.")
async def echo(ctx, *, message: str):
    await ctx.send(message)

# Command: Hello
@bot.command(name="hello", description="Greets the user.")
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.mention}! 👋")

# Command: Support ticket
@bot.command(name="support", description="Raise a ticket for bot-related issues.")
async def support(ctx):
    await ctx.send(f"To report bot issues, please contact support via email at `support@darkdeity.com`.")

# Command: Contact admin
@bot.command(name="contact", description="Displays contact information for the server admin.")
async def contact(ctx):
    await ctx.send("For server-related issues, please contact the admin: `admin@darkdeity.com`.")

# Command: Server info
@bot.command(name="info", description="Provides information about the server.")
async def info(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"Information about {guild.name}", color=0x0000ff)
    embed.add_field(name="Server Name", value=guild.name, inline=False)
    embed.add_field(name="Total Members", value=guild.member_count, inline=False)
    await ctx.send(embed=embed)

# Command: Ping
@bot.command(name="ping", description="Checks the bot's response time to Discord.")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")

# Command: Clear messages
@bot.command(name="clear", description="Deletes a specified number of messages from a channel.")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, number: int):
    await ctx.channel.purge(limit=number)
    await ctx.send(f"Deleted {number} messages!", delete_after=5)

# Run the bot
bot.run(BOT_TOKEN)
