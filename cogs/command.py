from discord.ext import commands, tasks
import discord
import argparse
import re
import datetime
import os

import base


class ParrotReturn(base.Command):
    class ReturnWin(base.Window):
        def __init__(self):
            super().__init__()

    def __init__(self, bot):
        super().__init__(windows=[self.ReturnWin()])
        self.parser.add_argument('sentence')

    @commands.command()
    async def parrot(self, ctx: commands.Context, *args):
        if self.parse(args):
            self.windows[0].set_embed(discord.Embed(
                title='Parrot',
                description=self.args.sentence
            ))

        else:
            self.windows[0].set_embed(discord.Embed(
                title='Parrot',
                description=self.parser.usage
            ))

        await self.send(0, channel=ctx.channel)


async def setup(bot):
    print('loaded')
    await bot.add_cog(ParrotReturn(bot))
