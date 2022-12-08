from discord.ext import commands, tasks
import discord
import argparse
import re
import datetime
import os

#TOKEN = os.getenv('DISCORD_BOT_TOKEN')
TOKEN = 'MTAyNzE2OTA5NjQyMjQwODI0Mw.GYdvjw.KYVNrVLsf2FX0k_SlY_k67waZ5HfWrV8yTQFFs'
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

#basic commands and message class
class Window(commands.Cog):
    def __init__(self, _bot):
        self.bot = _bot
        self.embed: discord.Embed = None
        self.message: discord.Message = None
        self.reactions = []
        #emoji
        self.emojis = []
        self.emoji_codes = []
        #parser for commands on discord
        self.parser = argparse.ArgumentParser()
        self.args = None

    def parse(self, _args):
        try:
            self.args = self.parser.parse_args(args=_args)
            return True
        except SystemExit:
            return False

    async def send(self, channel: discord.TextChannel):
        self.message = await channel.send(embed=self.embed)
        for i in self.emojis:
            self.reactions.append(await self.message.add_reaction(emoji=i))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        pass


class Poll(Window):
    def __init__(self, _bot):
        super().__init__(_bot=_bot)
        self.emojis = [':zero:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:',
                       ':seven:', ':eight:', ':nine:', ':keycap_ten:']
        self.emoji_codes = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

    async def send(self, channel: discord.TextChannel, *args, title='title', description='description'):
        self.embed = discord.Embed(color=0x1e90ff, title=title, description=description)

        for i in range(len(args[0])):
            self.embed.add_field(name=self.emojis[i], value=args[0][i], inline=False)

        self.message = await channel.send(embed=self.embed)
        for i in range(len(args[0])):
            self.reactions.append(await self.message.add_reaction(emoji=self.emoji_codes[i]))

    @commands.command()
    async def poll(self, ctx, *args):
        await self.send(ctx.channel, args)


class PoopGeneratorWin(Window):
    def __init__(self, _bot):
        super().__init__(_bot)
        self.embed = discord.Embed(color=0x8b4513, title='Poop Generator')
        self.embed.set_thumbnail(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/twitter/322/pile-of-poo_1f4a9.png')
        self.emojis.append('\N{pile of poo}')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return
        if reaction.message == self.message:
            if reaction.emoji == self.emojis[0]:
                await reaction.message.channel.send(':poop:')
                await reaction.remove(user)

    @commands.command()
    async def poop(self, ctx):
        await self.send(ctx.channel)


class Reserve(Window):
    def __init__(self, _bot):
        super().__init__(_bot=_bot)
        self.dt_reserved = None
        self.parser.add_argument('--title', default='title')
        self.parser.add_argument('--description', default='description')
        self.parser.add_argument('--time', default='now')

    async def notice(self, channel):
        pass

    async def parse_time(self, time):
        times = re.split('[/-]', time)
        self.dt_reserved = datetime.datetime(int(times[0]), int(times[1]), int(times[2]),
                                             int(times[3]), int(times[4]), int(times[5]))

    @commands.command()
    async def reserve(self, ctx, *_args):
        if self.parse(_args=_args):
            if self.args == 'now':
                await self.notice(ctx.channel)

            else:
                await self.parse_time(self.args.time)
                self.embed = discord.Embed(color=0x3cb371, title=self.args.title,
                                       description=self.args.description)
                await self.send(ctx.channel)
        else:
            await ctx.send("error")

    @tasks.loop(minutes=1.0)
    async def check_date(self):
        pass


async def on_studygroup_voice(member, before, after):
    if after.channel is not None and after.channel.id == 1030335762295693365:
        ch_notice = bot.get_channel(1030765503590969414)
        if before.channel is None and len(after.channel.members) == 1:
            embed = discord.Embed(color=0x4169e1, title='勉強会を開始しました！！',
                                  description='Laz「がんばれ！！！」\n@here')
            embed.set_author(name=member)
            embed.set_thumbnail(url='https://zetadivision.com/wp-content/uploads/2020/04/ZETADIVISION_Laz_square-1.jpg')
            await ch_notice.send(embed=embed)


@bot.event
async def on_voice_state_update(member, before, after):
    await on_studygroup_voice(member, before, after)


@bot.event
async def on_ready():
    print('Ready!')

bot.add_cog(PoopGeneratorWin(bot))
bot.add_cog(Poll(bot))
bot.add_cog(Reserve(bot))
bot.run(TOKEN)

print('test')
