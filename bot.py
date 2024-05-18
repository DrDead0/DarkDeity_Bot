import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(
    command_prefix='!',
    intents=intents
    )
bot.remove_command('help')

@bot.command(name="hello", description="returns hello")
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command(name="ping", description="returns latency")
async def ping(ctx):
    await ctx.send(f'{round(bot.latency * 1000)}ms')

@bot.command(name="help",description="return displayHelp")
async def help(ctx):
    Embed = discord.Embed(
        title="Help Menu",
        description=f"""
        Moderation\n
        !kick - Use to kick  \n
        !ban - -Use to ban \n
        !timeout - Use to mute \n
        !report - Use to report
         """ ,
        color=0xff0000)
                
    await ctx.send(embed=Embed)

bot.run('MTI0MTM2OTUzODYzNzk4NzkzMA.GukRTP.MLxJZUtOi93FW8Pu8FgTjTgzwmLxKSF_2rvaiA')