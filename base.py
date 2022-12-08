from discord.ext import commands, tasks
import discord
import argparse
import re
import datetime
import os


TOKEN = os.getenv('DISCORD_BOT_TOKEN')
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())


# コマンドの基本的なクラス　コマンドを管理するクラスはこれを継承する
class Command(commands.Cog):
    def __init__(self):
        pass

    @commands.command()
    async def test(self, ctx):
        ctx.send('test')


await bot.add_cog(Command(bot))
await bot.start(TOKEN)
