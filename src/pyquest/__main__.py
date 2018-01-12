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
import tempfile
from zipfile import ZipFile

from pyquest.game import QuestGame

file_name = sys.argv[1]

if file_name[-4:] == ".zip" or file_name[-6:] == ".quest":
    print("Opening QUEST file...")
    zipped = ZipFile(file_name, 'r')
    game_folder = tempfile.mkdtemp()
    zipped.extractall(game_folder)
    zipped.close()
    print(game_folder)
    os.system('ls -lah ' + game_folder)
    the_game = QuestGame(game_folder, from_qfile=True)
    the_game.run()
    os.system('rm -rf ' + game_folder)
else:
    the_game = QuestGame(sys.argv[1], from_qfile=False)