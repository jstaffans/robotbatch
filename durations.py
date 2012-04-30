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

class Durations(object):

    def __init__(self):
        self._result_files = []

    def add_result_file(self, file):
        self._result_files.append(file)

    def get_result_files(self):
        return self._result_files

    def parse_results(self):
        for result_file in self._result_files:
            results_xml = xml.parse(result_file)
            for child in results_xml.getiterator():
                print child
                print "\n"

    def get_suites(self):
        return [] 
