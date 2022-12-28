import sys
from lark import Lark
from lark import Transformer
from functools import reduce

class CommandParser:

    def __init__(self) -> None:
        self.argments = []

    def add_argument(self, name):
        self.argments.append(name)
        self.__dict__[name] = None

    def find_positional_arg(self):
        pass

    def find_optional_arg(self, arg):
        pass

    def parse_args(self, args):
        pass





class CommandTransformer(Transformer):
    def statement(self, tree):
        return

    def positional(self, tree):
        return

    def optional(self, tree):
        return

    def word(self, tree):
        return tree[0].lower()

    def letter(self, tree):
        return tree[0].lower()

args = sys.argv
text = args[1]
with open("test.lark", encoding="utf-8") as grammar:
    parser = Lark(grammar.read())
    tree = parser.parse(text)
    print(tree.pretty())