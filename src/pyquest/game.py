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

from pyquest.script_engine import Script
from pyquest.world_model import QuestObject


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
            exit(127)

        tmp = game.read()
        game_txt = tmp.decode('utf-8', errors='ignore')
        while game_txt[0] != '<':
            game_txt = game_txt[1:]

        # self.tree = ET.parse(self.game_file)
        self.root = ET.fromstring(game_txt)
        if self.debug:
            print("Successfully read in ASLX file.")

        self.objects = {}
        self.name = "No Name"
        self.gameid = "UNKNOWN"
        self.version = "UNKNOWN"
        self.firstpublished = "UNKNOWN"
        self.subtitle = ""
        self.author = "Anonymous"
        self.category = "None"
        self.description = ""
        self.cover = None
        self.startup = None
        self.settings = {}

        if self.debug:
            print("Beginning ASLX/XML tree traversal.")
        for element in self.root:
            if self.debug:
                print(element)
            if element.tag == "game":
                self.name = element.attrib["name"]
                for attr in element:
                    if attr.tag == "attr":
                        if attr.attrib["type"] == "boolean":
                            self.settings[attr.attrib["name"]] = (attr.text == "true")
                        elif attr.attrib["type"] == "int":
                            self.settings[attr.attrib["name"]] = int(attr.text)
                        else:
                            self.settings[attr.attrib["name"]] = attr.text
                        if self.debug:
                            print("Set game option", attr.attrib["name"], "to",
                                  self.settings[attr.attrib["name"]])
                    elif attr.text is None and attr.attrib == {}:
                        self.settings[attr.tag] = True
                        if self.debug:
                            print("Set flag", attr.tag)
                    elif attr.tag == "start":
                        if attr.attrib.get("type", None) == "script":
                            self.startup = Script(attr.text)
                        else:
                            self.startup = attr.text
                        if self.debug:
                            print("Set startup output to", self.startup)
                    elif attr.tag in {"gameid", "version", "firstpublished", "subtitle", "author",
                                      "category", "description", "cover"}:
                        self.__setattr__(attr.tag, attr.text)
                        if self.debug:
                            print("Set bibliographical info", attr.tag, "to", attr.text)
                    else:
                        self.settings[attr.tag] = attr.text
                        if self.debug:
                            print("Set game option", attr.tag, "to", self.settings[attr.tag])
            if element.tag == "object":
                self.create_object(element)
            # TODO: Handle other types of tags
        if self.debug:
            print("Done traversing ASLX/XML tree.")

    def run(self):
        print("Welcome to", self.name, "by", self.author, "version", self.version)
        if isinstance(self.startup, Script):
            self.startup.call()
        elif self.startup is not None:
            print(self.startup)
        pass

    def create_object(self, tag, parent_obj=None):
        attributes = {
            "inherit": []
        }
        delayed_children = []
        for attr in tag:
            if attr.tag == "object":
                delayed_children.append(attr)
            elif attr.text is None and attr.attrib == {}:
                attributes[attr.tag] = True
            elif attr.tag == "inherit":
                attributes['inherit'].append(attr.attrib['name'])
            else:
                the_type = attr.attrib.get('type', None)
                if the_type == "script":
                    attributes[attr.tag] = Script(attr.text)
                elif the_type == "boolean":
                    attributes[attr.tag] = (attr.text == "True")
                elif the_type == "stringlist":
                    values = []
                    for item in attr:
                        if item.tag == "value":
                            values.append(item.text)
                    attributes[attr.tag] = values
                else:
                    attributes[attr.tag] = attr.text
        attributes['parent'] = parent_obj
        name = tag.attrib['name']
        self.objects[name] = QuestObject(name, **attributes)
        if self.debug:
            print("Created:", self.objects[name])
        for child in delayed_children:
            self.create_object(child, self.objects[name])
