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

import os, sys, shutil
from random import shuffle
import operator
import durations, batchsplitter

def print_help():
    print __doc__

def print_usage():
    print 'Usage: robotbatch.py <number of batches> <output dir> <input xml file> ...'
    print 'Where:'
    print '       output dir     = parent directory of Robot test suites'
    print '       input xml file = Robot result XML file. You can enter as many files as you want.'

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print_usage()
    else:
        num_batches = int(sys.argv[1])
        d = durations.Durations()

        for result_file in sys.argv[3:]:
            print "Processing " + result_file + " ..."
            d.add_result_file(result_file)

        d.parse_results()
        
        bs = batchsplitter.BatchSplitter(d.get_durations())
        bs.split(num_batches)

        print '\nBATCHES:'
        print '--------'

        batches = bs.get_batch_durations()
        suites_to_batches = bs.get_suites_to_batches()
        
        for batch in sorted(batches.iterkeys()):
            print '%(batch)s (%(duration)d ms):' % {'batch': batch, 'duration': batches[batch]}
            for suite in suites_to_batches.iterkeys():
                if suites_to_batches[suite] == batch:
                    print '  %s' % suite

        robot_dir = sys.argv[2]
        print "\nNow scanning %s ...\n" % robot_dir

        dirs_to_batches = {}
        unknown_dirs = [] 

        for dirname, dirnames, filenames in os.walk(robot_dir):
            for subdirname in dirnames:
                current_dir = os.path.join(dirname,subdirname)
                current_dir_batch = False
                for suite in suites_to_batches.iterkeys():
                    if current_dir.lower().endswith(suite.lower()):
                        current_dir_batch = suites_to_batches[suite]
                        break
                if current_dir_batch == False:
                    unknown_dirs.append(current_dir)
                else:
                    dirs_to_batches[current_dir] = current_dir_batch

        if len(unknown_dirs) > 0:
            print 'The following directories could not be mapped to a batch - '
            print 'if they contain tests you will have add them manually:'
            print '------------------------------------------------------'

            for unknown_dir in unknown_dirs: 
                print unknown_dir

            print '------------------------------------------------------\n'
            
        print "Ready to assign directories to batches via __init__.txt files."
        print "Old __init__.txt files will be backed up and overwritten."
        print "Target directory is %s." % robot_dir
        update_init_files = raw_input("Continue? [y/N]: ").strip()
        if update_init_files.lower() != "y":
            exit()

        for suite_dir in dirs_to_batches:
            init_file = os.sep.join([suite_dir, '__init__.txt'])
            if os.path.isfile(init_file):
                shutil.copyfile(init_file, init_file + '.old')            
            f = open(init_file, 'w')
            f.write('*** Settings ***\n\n')
            f.write('Force Tags  %s\n' % dirs_to_batches[suite_dir])
            f.close()
