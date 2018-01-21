from pyquest.script_engine import QuestValue

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


class QuestObject:
    def __init__(self, name, **kwattribs):
        self.__dict__ = kwattribs
        self.name = name

    def __str__(self):
        return "Object {} with attributes {}".format(self.name, self.__dict__)

    def __setattr__(self, key, value):
        if isinstance(value, int) or isinstance(value, str) or isinstance(value, float):
            object.__setattr__(self, key, QuestValue(value))
        else:
            object.__setattr__(self, key, value)
