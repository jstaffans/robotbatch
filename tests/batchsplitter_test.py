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
import batchsplitter

class BatchSplitterTest(unittest.TestCase):

    def test_num_suites_equals_num_batches(self):
        bs = batchsplitter.BatchSplitter({'Suite1' : 1, 'Suite2' : 1, 'Suite3' : 1})
        bs.split(3)
        batches = bs.get_batch_durations()
        self.assertEqual(3, len(batches))
        for batch in batches:
            self.assertEqual(1, batches[batch])
   
    def test_single_batch(self):
        bs = batchsplitter.BatchSplitter({'Suite1' : 1, 'Suite2' : 1, 'Suite3' : 1})
        bs.split(1)
        batches = bs.get_batch_durations()
        self.assertEqual(1, len(batches))
        self.assertEqual(3, batches['Batch0'])

    def test_best_split_is_found(self):
        bs = batchsplitter.BatchSplitter({'Suite1' : 2, 'Suite2' : 5, 'Suite3' : 1, 'Suite4' : 4, 'Suite5': 3})
        bs.split(3)
        batches = bs.get_batch_durations()
        self.assertEqual(3, len(batches))
        
        for batch in batches:
            self.assertEqual(5, batches[batch])

        suites_to_batches = bs.get_suites_to_batches()
        self.assertEqual(5, len(suites_to_batches))
        self.assertEqual(True, suites_to_batches['Suite1'] == suites_to_batches['Suite5'])
        self.assertEqual(True, suites_to_batches['Suite3'] == suites_to_batches['Suite4'])

if __name__ == '__main__':
    unittest.main()

