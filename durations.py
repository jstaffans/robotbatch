# Copyright 2012 Johannes Staffans
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import xml.etree.ElementTree as xml
import os

class Durations(object):

    def __init__(self):
        self._result_files = []
        self._durations = {} 

    def add_result_file(self, file):
        self._result_files.append(file)

    def get_result_files(self):
        return self._result_files

    def parse_results(self):
        for result_file in self._result_files:
            suitestack = []
            for (event, node) in xml.iterparse(result_file, ['start', 'end']):
                if event == 'end' and node.tag == 'entry':
                    suitestack.pop()

                if event == 'start':
                    if node.tag == 'entry':
                        suitestack.append('%suite%')
                    if node.tag == 'string' and suitestack[-1] == '%suite%':
                        suitestack.pop()
                        suitestack.append(node.text)
                    if node.tag == 'duration' and node.text != None:
                        self.add_duration(suitestack, node.text)

    def add_duration(self, suitestack, duration):
        key = os.sep.join(suitestack[0:-2])
        if key in self._durations:
            self._durations[key] += int(duration)
        else:
            self._durations[key] = int(duration)

    def get_durations(self):
        return self._durations 

