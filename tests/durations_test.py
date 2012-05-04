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

import unittest
import durations

class DurationsTest(unittest.TestCase):

    def test_result_file_addition(self):
        d = durations.Durations()
        d.add_result_file('foo')
        d.add_result_file('bar')
        self.assertEqual(2, len(d.get_result_files()))
        self.assertEqual('foo', d.get_result_files()[0])
        self.assertEqual('bar', d.get_result_files()[1])

    def test_suite_parsing(self):
        d = durations.Durations()
        d.add_result_file('tests/robot_results.xml')
        d.parse_results()
        self.assertEqual(2, len(d.get_durations()))
        self.assertEqual(27263, d.get_durations()['Ui/CalendarTests'])
        self.assertEqual(11947, d.get_durations()['Ui/PersonTests'])


if __name__ == '__main__':
    unittest.main()
