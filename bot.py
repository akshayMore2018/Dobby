import discord
from discord.ext import commands
import random
import config

client = commands.Bot(command_prefix='.')

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
		await client.say(config.ERROR)


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
		await client.say(config.ERROR)

@client.event
async def on_message_delete(message):
	author=message.author
	content=message.content
	channel=message.channel
	#await client.send_message(channel,"{} : {}".format(author,content))
	


client.run(config.TOKEN)

