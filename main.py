import discord
from discord.ext import commands
from openrouter import mimicPrompt, comment
from mongoDB import checkUserExist, createUser, updateUserPrompt, checkValidTokens, useToken, getPrompt, selectUser, getSelectedUser
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

fake_cache = {}

@bot.command()
async def mimic(ctx, target_username, overwrite=None):
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
                prompt = await clonePersonality(ctx, target_member) 
                createUser(target_id, prompt, target_username)
                useToken(ctx.author.id)
                await ctx.send("successfully copied user identity!")
            else:
                await ctx.send("You are out of tokens, try again tomorrow.")
                return
    elif( overwrite == 'overwrite'):
        if checkValidTokens(ctx.author.id):
                prompt = await clonePersonality(ctx, target_member) 
                updateUserPrompt(target_id, prompt)
                useToken(ctx.author.id)
                await ctx.send("successfully overwrote user identity!")
        else:
                await ctx.send("You are out of tokens, try again tomorrow.")
                return
    
    selectUser(ctx.guild.id, target_id)
    await ctx.guild.me.edit(nick=f'I am {target_member.display_name}')
    await ctx.send("User Selected!")


@bot.command()
async def glaze(ctx):
    if checkValidTokens(ctx.author.id):
        await ctx.message.delete()
        previous_message = ""
        async for message in ctx.channel.history(limit=1, before=ctx.message):
            previous_message = message.content

        selectedUserID = getSelectedUser(ctx.guild.id)
        if selectedUserID== None:
            await ctx.send("select a user!")
            return

        prompt = getPrompt(selectedUserID)
        message = comment("glaze", prompt, previous_message)
        await ctx.send(message)
        useToken(ctx.author.id)
    else:
        await ctx.send("You are out of tokens, try again tomorrow.")
        return 

@bot.command()
async def roast(ctx):
    if checkValidTokens(ctx.author.id):
        await ctx.message.delete()
        previous_message = ""
        async for message in ctx.channel.history(limit=1, before=ctx.message):
            previous_message = message.content

        selectedUserID = getSelectedUser(ctx.guild.id)
        if selectedUserID == None:
            await ctx.send("select a user!")
            return

        prompt = getPrompt(selectedUserID)
        message = comment("roast", prompt, previous_message)
        await ctx.send(message)
        useToken(ctx.author.id)
    else:
        await ctx.send("You are out of tokens, try again tomorrow.")
        return 
    


async def clonePersonality(ctx, target_member):
    messages = []
    async for message in ctx.channel.history(limit=500, before=ctx.message):
        if message.author == target_member and len(message.content) < 55:
            try:
                messages.append(message.content)
            except UnicodeEncodeError:
                print("message has special characters")
    prompt = mimicPrompt(messages)
    return prompt



bot.run(TOKEN)