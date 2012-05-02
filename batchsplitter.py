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

from random import shuffle
import operator

class BatchSplitter(object):

    def __init__(self, suites_with_durations):
        self._suites_with_durations = suites_with_durations

    def split(self, num_batches):
        suite_names = [suite for suite in self._suites_with_durations]
        
        self._current_split = {}
        self._current_suite_to_batch = {}

        for i in range(1000):
            shuffle(suite_names)
            batches = self._split_by_duration(suite_names, num_batches)
            if self._is_better_than_current_split(batches):
                self._set_current_split(batches)

    def _split_by_duration(self, suite_names, num_batches):
        batches = {}
        self._suite_to_batch = {}
        for batch_id in range(num_batches):
            batches['Batch%d' % batch_id] = 0

        for suite in suite_names:
            suite_duration = self._suites_with_durations[suite]
            sorted_batches = sorted(batches.iteritems(), key=operator.itemgetter(1))
            batch, current_batch_duration = sorted_batches[0]
            batches[batch] += suite_duration
            self._suite_to_batch[suite] = batch 

        return batches

    def _is_better_than_current_split(self, batches):
        if len(self._current_split) == 0:
            return True

        current_min_max_diff = self._get_min_max_diff(self._current_split)
        new_min_max_diff = self._get_min_max_diff(batches)

        return new_min_max_diff < current_min_max_diff

    def _get_min_max_diff(self, batches):
        sorted_batches = sorted(batches.iteritems(), key=operator.itemgetter(1))
        minId, minVal = sorted_batches[0]
        maxId, maxVal = sorted_batches[-1]
        return (maxVal - minVal)

    def _set_current_split(self, batches):
        self._current_split = batches
        self._current_suite_to_batch = self._suite_to_batch
        
    def get_batch_durations(self):
        return self._current_split

    def get_suites_to_batches(self):
        return self._current_suite_to_batch
