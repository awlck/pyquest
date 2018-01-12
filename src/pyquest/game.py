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
import sys
import xml.etree.ElementTree as ET


class QuestGame:
    def __init__(self, game_file, launch_dir=None, from_qfile=True, debug=False):
        self.debug = debug
        if from_qfile:
            file_name = game_file + os.path.sep + "game.aslx"
            self.game_folder = game_file
        else:
            file_name = game_file
            self.game_folder = os.path.sep.join(os.path.split(game_file)[:-1])

        if launch_dir is not None:
            self.launch_dir = launch_dir
        else:
            self.launch_dir = self.game_folder
        if self.debug:
            print("Attempting to read", file_name, "with launch dir", self.launch_dir,
                  "from packed Quest file" if from_qfile else "in raw mode.")
        try:
            game = open(file_name, 'rb')
        except FileNotFoundError as e:
            print("*** I was unable to read the game file", game_file, file=sys.stderr)

        tmp = game.read()
        game_txt = tmp.decode('utf-8', errors='ignore')
        while game_txt[0] != '<':
            game_txt = game_txt[1:]

        # self.tree = ET.parse(self.game_file)
        self.root = ET.fromstring(game_txt)
        if self.debug:
            print("Successfully parsed ASLX file.")

    def run(self):
        for element in self.root:
            print(element)