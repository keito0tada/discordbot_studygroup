from discord.ext import commands, tasks
import discord
import argparse
import re
import datetime
import os


# super class of all windows
# we must use when we send any messages to users
class Window:
    def __init__(self, embed: discord.Embed = None, view: discord.ui.View = None, buttons: list[discord.ui.Button] = None):
        self.embed = embed
        self.view = view
        self.buttons = buttons

    def set_embed(self, embed: discord.Embed):
        self.embed = embed

    def set_view(self, view: discord.ui.View):
        self.view = view

    async def send(self, channel: discord.TextChannel):
        await channel.send(embed=self.embed, view=self.view)


# super class of all commands
class Command(commands.Cog):
    def __init__(self, windows: list[Window]):
        # Command has some windows. Choose and send a window when responding users.
        self.windows = windows
        # argparse for splitting commands args by user
        self.parser = argparse.ArgumentParser(exit_on_error=False)
        self.args = None
        # is command executing?
        self.is_executing = False

    def parse(self, args):
        try:
            self.args = self.parser.parse_args(args=args)
            return True

        except SystemExit:
            print('errorrrrr')
            return False


    async def send(self, ind_window: int, channel: discord.TextChannel):
        await self.windows[ind_window].send(channel=channel)

