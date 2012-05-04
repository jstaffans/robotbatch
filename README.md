robot-batch
===========

Tool for splitting robot test suites into batches for parallell execution.
Suites are split empirically according to their durations. Test suite durations
are gathered from the robot_results.xml files of a previous test run.

Usage: robotbatch.py <number of batches> <output dir> <input xml file> ...
Where: 
       output dir     = parent directory of Robot test suites.
       input xml file = Robot result XML file. You can enter as many files as you want.

Suites are assigned to batches called Batch1, Batch2 and so on. The assignment happens
through a Force Tags setting in the suite's __init__.txt file.

Note that only top level suites are processed. If you have a test suite layout like this:

PersonTests
PersonTests/List
CalendarTests

Then there would be two suites that can be split into batches (PersonTests and CalendarTests).
PersonTests/__init__.txt and CalendarTests/__init__.txt would be updated.


