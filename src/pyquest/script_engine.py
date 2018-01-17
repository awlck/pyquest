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

import os
from shutil import get_terminal_size
from time import sleep


class Script:
    def __init__(self, code):
        self.code = code

    def call(self):
        print("Code Execution not fully implemented.")
        print("Launching the perhaps ugliest parser to date....")
        lines = self.code.splitlines()
        i = 0
        while i < len(lines):
            words = lines[i].split()
            if len(words) == 0:
                i += 1
                continue
            if words[0] == "msg":
                eval("print " + " ".join(words[1:]))
                i += 1
                continue
            if words[0] == "PrintCentered":
                eval("print_centered " + " ".join(words[1:]))
                i += 1
                continue
            if words[0] == "ClearScreen":
                os.system("cls" if os.name == "nt" else "clear")
                i += 1
                continue
            if words[0] == "wait":
                input("Press ENTER to continue... ")
                i += 1
                continue
            if words[0] == "SetTimeout":
                eval("sleep" + words[1])
            # Unknown content
            # raise NotImplementedError("I did not understand this code line: " + lines[i])
            i += 1
            continue

    def __str__(self):
        return "({} characters of code)".format(len(self.code))

    def __repr__(self):
        return self.__str__()


class Verb:
    def __init__(self, verb):
        self.verb = verb


def print_centered(text):
    print(text.center(get_terminal_size()[0] - 1))
