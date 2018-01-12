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
    def __init__(self, game_file, launch_dir=None, from_qfile=True):
        if from_qfile:
            file_name = game_file + os.path.sep + "game.aslx"
            self.game_folder = game_file
        else:
            file_name = game_file
            self.game_folder = os.path.sep.join(os.path.split(game_file)[:-1])

        try:
            self.game_file = open(file_name)
        except FileNotFoundError as e:
            print("*** Could not read game file", game_file, file=sys.stderr)

        if launch_dir is not None:
            self.launch_dir = launch_dir
        else:
            self.launch_dir = self.game_folder

        self.tree = ET.parse(self.game_file)
        self.root = self.tree.getroot()

    def __del__(self):
        self.game_file.close()

    def run(self):
        for element in self.root:
            print(element)