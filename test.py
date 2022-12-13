import discord
from discord.ext import commands


TOKEN = 'MTAyNzE2OTA5NjQyMjQwODI0Mw.G4ckTQ.oQNoNdun-UzNzIN0crYiJzReH4fLmtgqdWAde0'

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all()) 


@bot.event
async def on_message(message):
	view = discord.ui.View(timeout=180.0)
	view.add_item(discord.ui.Button(url='https://google.com', emoji='😊'))
	await message.channel.send(view=view)


bot.run(TOKEN)
