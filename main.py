import discord
from discord.ext import commands
from openrouter import mimicPrompt, comment
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

fake_cache = {}
current_glazer = None

@bot.command()
async def mimic(ctx, username):
    global current_glazer
    member = ctx.guild.get_member_named(username)
    if member == None:
        await ctx.send("User Not Found!")
        return
    
    messages = []
    async for message in ctx.channel.history(limit=200, before=ctx.message):
        if message.author == member:
            try:
                messages.append(message.content)
            except UnicodeEncodeError:
                print("message has special characters")
    
    fake_cache[member.id] = mimicPrompt(messages)
    current_glazer = member
    await ctx.guild.me.edit(nick=current_glazer.display_name)
    await ctx.send("successfully copied user identity!")

@bot.command()
async def glaze(ctx):

    await ctx.message.delete()

    previous_message = ""
    async for message in ctx.channel.history(limit=1, before=ctx.message):
        previous_message = message.content
    message = comment("glaze", fake_cache[current_glazer.id], previous_message)

    await ctx.send(message)

@bot.command()
async def roast(ctx):

    await ctx.message.delete()

    previous_message = ""
    async for message in ctx.channel.history(limit=1, before=ctx.message):
        previous_message = message.content
    message = comment("roast", fake_cache[current_glazer.id], previous_message)

    await ctx.send(message)






bot.run(TOKEN)