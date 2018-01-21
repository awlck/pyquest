from html.parser import HTMLParser
from shutil import get_terminal_size

import pyquest.game

__author__ = "Adrian Welcker"
__copyright__ = """Copyright 2018 Adrian Welcker

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""


class QuestValue:
    """Union[str, int, float], sort of."""
    def __init__(self, value):
        if not (isinstance(value, int) or isinstance(value, float) or isinstance(value, str)):
            raise TypeError("QuestValue cannot accept type " + str(type(value)))
        self._value = value

    # def __instancecheck__(self, instance):
    #     return isinstance(self._value, instance)

    def __add__(self, other):
        if (isinstance(self._value, int) or isinstance(self._value, float)) and \
                (isinstance(other, int) or isinstance(other, float)):
            return self._value + other
        elif (isinstance(self._value, int) or isinstance(self._value, float)) and \
                isinstance(other, QuestValue):
            if isinstance(other._value, int) or isinstance(other._value, float):
                return self._value + other._value
            elif isinstance(other._value, str):
                return str(self._value) + other._value
        elif isinstance(self._value, str) and isinstance(other, str):
            return self._value + other
        elif isinstance(self._value, str):
            return self._value + str(other)
        else:
            raise TypeError("QuestValue: operation add not supported for self (" +
                            str(type(self._value)) + ") and other (" + str(type(other)) + ").")

    def __radd__(self, other):
        if (isinstance(other, int) or isinstance(other, float)) and \
                (isinstance(self._value, int) or isinstance(self._value, float)):
            return other + self._value
        elif isinstance(other, QuestValue) and (isinstance(self._value, int) or
                                                isinstance(self._value, float)):
            if isinstance(other._value, int) or isinstance(other._value, float):
                return other._value + self._value
            elif isinstance(other._value, str):
                return str(other._value) + str(self._value)
        elif isinstance(other, str) and isinstance(self._value, str):
            return other + self._value
        elif isinstance(self._value, str):
            return str(other) + self._value
        elif isinstance(other, str):
            return other + str(self._value)
        elif isinstance(other, QuestValue):
            return repr(other._value) + repr(self._value)
        else:
            raise TypeError("QuestValue: operation add not supported for other (" +
                            str(type(other)) + ") and self (" + str(type(self._value)) + ").")

    def __repr__(self):
        if isinstance(self._value, str):
            return self._value
        else:
            return repr(self._value)

    def __str__(self):
        if isinstance(self._value, str):
            return self._value
        else:
            return str(self._value)


class QuestList(list):
    def __init__(self, type_):
        super(QuestList, self).__init__()
        self._type = type_


class ScriptEngine:
    def __init__(self, game):
        self.game = game
        self.functions = {}

    def define_function(self, name, *params, body):
        self.functions[name] = Function(name, *params, body=body)

    def is_function(self, name):
        return name in self.functions

    def prep(self):
        globals().update(pyquest.game.the_game.objects)
        globals().update(self.functions)


class Function:
    def __init__(self, name, *params, body):
        self.name = name
        self.parameters = params
        self.body = body

    def __call__(self, *params):
        Script("functions->" + self.name, self.body)(**dict(zip(self.parameters, params)))


class Script:
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __call__(self, **kwparams):
        # pylint:disable=exec-used,eval-used
        result = None  # variable holding the result of "get input" and "ShowMenu" directives
        print("Code Execution not fully implemented.")
        print("Launching the perhaps ugliest parser to date....", self.name)
        if len(kwparams) != 0:
            print(kwparams)
            for tag, val in kwparams.items():
                if isinstance(val, str):
                    definer = tag + ' = """' + val + '"""'
                else:
                    definer = tag + " = " + repr(val)
                exec(compile(definer, pyquest.game.the_game.name + "->" + self.name
                             + ": parameters", 'exec'))
        lines = self.code.splitlines()
        i = 0
        while i < len(lines):
            print("Now on line", i, "::", lines[i])
            words = lines[i].split()
            if len(words) == 0:
                i += 1
                continue

            # TODO: REMOVE THIS, probably.
            if words[-1] == "{":
                del words[-1]

            # TODO: Stuff for if
            if len(words) > 1 and words[0] == "if":
                words[0] = "bool"
                for j in range(len(words)):
                    if words[j] == "=":
                        words[j] = "=="
                print("About to if-evaluate:", ' '.join(words))
                if eval(compile(' '.join(words), pyquest.game.the_game.name + "->"
                                + self.name + ": l" + str(i), 'eval')):
                    print(' '.join(words), ":: True")
                    # TODO: RUN IF BLOCK
                else:
                    print(' '.join(words), ":: False")
                    # TODO: RUN ELSE BLOCK
                i += 1
                continue
            if "else" in words:
                i += 1
                continue

            # TODO: -> Stuff for firsttime / otherwise
            # TODO: Stuff for loops

            if len(words) > 1 and words[0] == "foreach":
                the_iter = eval(words[2][:-1])
                for the_val in the_iter:
                    exec(words[1][1:-1] + " = the_val")
                    # TODO: Do stuff!
                    pass
                i += 1
                continue

            # TODO: Stuff for "built-ins"

            if len(words) > 2 and words[0] == "list" and words[1] == "add":
                words[0] = "list_add"
                del words[1]

            if len(words) == 1 and words[0] == "}":
                print("[** TODO: ADD CODE BLOCK HANDLING! **]")
                i += 1
                continue

            if len(words) == 1 and words[0] == "return":
                return
            if len(words) > 1 and words[0] == "return":
                return eval(compile(' '.join(words[1:]), pyquest.game.the_game.name + "->" +
                                    self.name + ": l" + str(i), 'eval'))

            exec(compile(' '.join(words), pyquest.game.the_game.name + "->" + self.name + ": l"
                         + str(i), 'exec'))
            i += 1
            continue

    def __str__(self):
        return "({} characters of code)".format(len(self.code))

    def __repr__(self):
        return "Script(name=%r, code=%r)" % (self.name, self.code)


class Verb:
    def __init__(self, verb):
        self.verb = verb


class MarkupStripper(HTMLParser):
    def error(self, message):
        print("[** HTML Markup Stripper Error:", message, "**]")

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = False
        self.fed = []

    def handle_data(self, data):
        self.fed.append(data)

    def get_data(self):
        return ''.join(self.fed)


def demarkup(text):
    stripper = MarkupStripper()
    stripper.feed(text.replace("<br/>", "\n").replace("<br>", "\n"))
    return stripper.get_data()


#
# def print_centered(text):
#     print(text.center(get_terminal_size()[0] - 1))


# pylint:disable=invalid-name
class FakeJS:
    """Provides methods for "JS.something( )" calls withing ASL source.

    Since we operate on a terminal instead of an HTML output,
    most of this does nothing.
    """
    def __init__(self):
        self.alignment = "left"

    def createNewDiv(self, align):
        """Sets the alignment to the given alignment."""
        self.alignment = align

    def StartOutputSection(self, name):
        """Does nothing."""
        pass

    def EndOutputSection(self, name):
        """Does nothing."""
        pass

    def HideOutputSection(self, name):
        """Does nothing."""
        pass


def msg(text):
    """Prints text to the screen, using the currently active alignment."""
    for line in text.splitlines():
        if JS.alignment == "left":
            print(demarkup(line))
        elif JS.alignment == "center":
            print(demarkup(line).center(get_terminal_size()[0] - 1))
        else:
            print(demarkup(line).rjust(get_terminal_size()[0] - 1))


def NewStringList():
    return QuestList("string")


def list_add(list_, value):
    list_.append(value)


def HasInt(obj, tag):
    try:
        return isinstance(getattr(obj, tag), int)
    except AttributeError:
        return False


def HasString(obj, tag):
    try:
        return isinstance(getattr(obj, tag), str)
    except AttributeError:
        return False


def TypeOf(obj):
    if isinstance(obj, QuestValue):
        if isinstance(obj._value, str):
            return "string"
        elif isinstance(obj._value, str):
            return "int"
    elif isinstance(obj, str):
        return "string"
    elif isinstance(obj, int):
        return "int"
    elif isinstance(obj, QuestList):
        return obj._type + "list"
    elif isinstance(obj, list):
        if len(obj) > 0:
            if isinstance(obj[0], str):
                return "stringlist"
            elif isinstance(obj[0], int):
                return "intlist"


JS = FakeJS()
false = False
true = True
null = None
LengthOf = len
