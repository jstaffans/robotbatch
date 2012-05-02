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
import durations

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
        
        temp_durations = d.get_durations()
        suites = []
        for suite, suite_duration in temp_durations.iteritems():
            suites.append(suite)
        
        best_suite_duration = {}
        best_suite_to_batch = {}
        min_max_difference = -1

        for i in range(1000):
            shuffle(suites)

            batches = {}
            suite_to_batch = {}
            for batch_id in range(num_batches):
                batches['Batch%d' % batch_id] = 0

            for suite in suites:
                suite_duration = temp_durations[suite]
                sorted_batches = sorted(batches.iteritems(), key=operator.itemgetter(1))
                batch, value = sorted_batches[0]
                batches[batch] += suite_duration
                suite_to_batch[suite] = batch 

            sorted_batches = sorted(batches.iteritems(), key=operator.itemgetter(1))
            minId, minVal = sorted_batches[0]
            maxId, maxVal = sorted_batches[-1]
            diff = maxVal - minVal
            if min_max_difference == -1 or  diff < min_max_difference:
                min_max_difference = diff
                best_suite_duration = batches
                best_suite_to_batch = suite_to_batch

        print best_suite_duration
        print best_suite_to_batch 

