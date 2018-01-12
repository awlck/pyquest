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

import xml.etree.ElementTree as ET


class QuestGame:
    def __init__(self, game_location, from_qfile=True):
        if from_qfile:
            self.game_file = open(game_location + "/game.aslx")
            self.game_folder = game_location
        else:
            self.game_file = open(game_location)
            self.game_folder = '/'.join(self.game_file.name.split('.')[:-1])
        self.tree = ET.parse(self.game_file)
        self.root = self.tree.getroot()

    def run(self):
        for element in self.root:
            print(element)