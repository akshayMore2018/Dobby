import discord
from discord.ext import commands
import asyncio
from itertools import cycle
import random
import config

client = commands.Bot(command_prefix='.')
client.remove_command("help")


#bot status
async def change_status():
	await client.wait_until_ready()
	msgs=cycle(config.STATUS)
	while not client.is_closed:
		current_status=next(msgs)
		await client.change_presence(game=discord.Game(name=current_status))
		await asyncio.sleep(60)

@client.event
async def on_ready():
	print("Dobby is ready Master.")

@client.event
async def on_message(message):
	author=message.author
	content=message.content
	channel=message.channel
	print("{} : {}".format(author,content))
	try:
		if content.lower().startswith("hello"):
			await client.send_message(channel,random.choice(config.WELCOME))
		await client.process_commands(message)
	except:
		await client.send_message(channel,config.ERROR)

@client.command(pass_context=True)
async def repeat(ctx,*args):
	try:
		author=ctx.message.author
		if author.id==config.MASTER:
			output=" "
			for words in args:
				output+=words
				output+=" "
			await client.say(output)
		else:
			await client.say("{} : {}".format(author,random.choice(config.ACCESS_DENIED)))
	except:
		await client.say("{} , {}".format(config.ERROR,"bot went offline."))
		await client.logout()


@client.command(pass_context=True)
async def clear(ctx,amount=10):
	try:	
		author=ctx.message.author
		if author.id==config.MASTER:
			channel=ctx.message.channel
			messages=[]
			async for message in client.logs_from(channel,limit=int(amount)):
				messages.append(message)
			await client.delete_messages(messages)
			await client.say("messages deleted")
		else:
			await client.say("{} : {}".format(author,random.choice(config.ACCESS_DENIED)))
	except:
		await client.say("{} , {}".format(config.ERROR,"bot went offline."))
		await client.logout()


@client.command(pass_context=True)
async def help(ctx):
	try:
		author=ctx.message.author
		embed=discord.Embed(
			colour=discord.Colour.orange()
		)
		embed.set_author(name="Help")
		embed.add_field(name=".repeat",value="repeats the line typed",inline=False)
		await client.send_message(author,embed=embed)
	except:
		await client.say("{} , {}".format(config.ERROR,"bot went offline."))
		await client.logout()
		

@client.event
async def on_message_delete(message):
	author=message.author
	content=message.content
	channel=message.channel
	#await client.send_message(channel,"{} : {}".format(author,content))
	

client.loop.create_task(change_status())
client.run(config.TOKEN)
