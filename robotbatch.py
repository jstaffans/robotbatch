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

import os, sys
from random import shuffle
import operator
import durations, batchsplitter

def print_help():
    print __doc__

def print_usage():
    print 'Usage: robotbatch.py <number of batches> <result files ...>'

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print_usage()
    else:
        num_batches = int(sys.argv[1])
        d = durations.Durations()
        for result_file in sys.argv[2:]:
            print "Processing " + result_file + " ..."
            d.add_result_file(result_file)

        d.parse_results()
        
        bs = batchsplitter.BatchSplitter(d.get_durations())
        bs.split(num_batches)

        print bs.get_batch_durations()
        print bs.get_suites_to_batches()

