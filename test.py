import sys
import typing
import re
from dataclasses import dataclass
import lark.exceptions
from lark import Lark
from lark import Transformer
from functools import reduce


class DuplicatedArgumentError(lark.exceptions.LarkError):
    pass


@dataclass
class Arg:
    name: str
    required: bool


class CommandParser:
    class CommandTransformer(Transformer):
        def statement(self, tree) -> (list, dict):
            if len(tree) == 0:
                return [], {}
            elif len(tree) == 1:
                if type(tree[0]) == dict:
                    return [], tree[0]
                else:
                    return tree[0], {}
            else:
                return tree[0], tree[1]

        def positionals(self, tree):
            if len(tree) == 1:
                return [tree[0]]
            else:
                tree[0].append(tree[1])
                return tree[0]

        def positional(self, tree):
            return tree[0]

        def optionals(self, tree):
            if len(tree) == 1:
                if len(tree[0]) == 1:
                    return {tree[0][0]: []}
                else:
                    return {tree[0][0]: tree[0][1:]}
            else:
                if tree[1][0] in tree[0]:
                    raise DuplicatedArgumentError
                else:
                    if len(tree[1]) == 1:
                        tree[0][tree[1][0]] = []
                    else:
                        tree[0][tree[1][0]] = tree[1][1:]

                    return tree[0]

        def optional(self, tree):
            if len(tree) == 1:
                return [tree[0]]
            else:
                return [i for i in tree]

        def word(self, tree):
            return tree[0].lower()

        def letter(self, tree):
            return tree[0].lower()

    def __init__(self) -> None:
        self.arguments: list[Arg] = []
        with open("test.lark", encoding="utf-8") as grammar:
            self.parser = Lark(grammar.read())

        self.tree: typing.Union[lark.Tree, None]= None
        self.result = None

    def isoptional(self, arg: str):
        return arg[0] == '-'

    def add_argument(self, name, required=False):
        self.arguments.append(self.Arg(name, required))

    def set_arguments(self):
        index = 0
        for i in self.arguments:
            if not self.isoptional(i.name):
                self.__dict__[i.name] = self.result[0][index]
                index += 1

        


    def parse_args(self, args: str):
        self.tree = self.parser.parse(args)
        print(self.tree.pretty())
        self.result = self.CommandTransformer().transform(self.tree)
        print(self.result)


commandparser = CommandParser()
commandparser.parse_args(sys.argv[1])