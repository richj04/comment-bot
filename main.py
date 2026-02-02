import discord
from discord.ext import commands
from openrouter import mimicPrompt, comment
from mongoDB import checkUserExist, createUser, updateUserPrompt, checkValidTokens, useToken
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
async def mimic(ctx, target_username):
    print("mimic function run!")
    #if user doesn't exist, create user
    if not checkUserExist(ctx.author.id):
        print("creating user ID")
        createUser(ctx.author.id, None)

    #check targetUser exist, if doesn't exist, check if they exist in server then creates userInstance   
    target_member = ctx.guild.get_member_named(target_username)
    print(target_member)
    if target_member == None:
            print("target member is none")
            await ctx.send("User Not Found!")
            return
    target_id = target_member.id
    if not checkUserExist(target_id):
            if checkValidTokens(ctx.author.id):
                prompt = clonePersonality(ctx, target_member) 
                createUser(target_id, prompt)
                useToken(ctx.author.id)
            else:
                await ctx.send("You are out of tokens, try again tomorrow.")
                return
    
    global current_glazer
    current_glazer = target_member
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


async def clonePersonality(ctx, target_member):
    messages = []
    async for message in ctx.channel.history(limit=200, before=ctx.message):
        if message.author == target_member:
            try:
                messages.append(message.content)
            except UnicodeEncodeError:
                print("message has special characters")
    prompt = mimicPrompt(messages)
    return prompt



bot.run(TOKEN)