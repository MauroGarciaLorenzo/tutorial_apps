#!/usr/bin/python
#
#  Copyright 2002-2019 Barcelona Supercomputing Center (www.bsc.es)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

# -*- coding: utf-8 -*-

import sys

from pycompss.api.task import task
from pycompss.api.parameter import *

FILENAME1 = "file1"
FILENAME2 = "file2"
FILENAME3 = "file3"


def main_program():
    # Check and get parameters
    if len(sys.argv) != 5:
        usage()
        exit(-1)
    N = int(sys.argv[1])
    counter1 = int(sys.argv[2])
    counter2 = int(sys.argv[3])
    counter3 = int(sys.argv[4])

    # Initialize counter files
    initializeCounters(counter1, counter2, counter3)
    print("Initial counter values:")
    printCounterValues()

    # Execute increment
    for i in range(N):
        increment(FILENAME1)
        increment(FILENAME2)
        increment(FILENAME3)

    # Write final counters state (sync)
    print("Final counter values:")
    printCounterValues()


def usage():
    print("[ERROR] Bad numnber of parameters")
    print("    Usage: increment <numIterations> " +
          "<counterValue1> <counterValue2> <counterValue3>")


def initializeCounters(counter1, counter2, counter3):
    # Write value counter 1
    fos = open(FILENAME1, 'w')
    fos.write(str(counter1))
    fos.close()

    # Write value counter 2
    fos = open(FILENAME2, 'w')
    fos.write(str(counter2))
    fos.close()

    # Write value counter 3
    fos = open(FILENAME3, 'w')
    fos.write(str(counter3))
    fos.close()


def printCounterValues():
    from pycompss.api.api import compss_open

    # Read value counter 1
    fis = compss_open(FILENAME1, 'r+')
    counter1 = fis.read()
    fis.close()

    # Read value counter 1
    fis = compss_open(FILENAME2, 'r+')
    counter2 = fis.read()
    fis.close()

    # Read value counter 1
    fis = compss_open(FILENAME3, 'r+')
    counter3 = fis.read()
    fis.close()

    # Print values
    print("- Counter1 value is " + str(counter1))
    print("- Counter2 value is " + str(counter2))
    print("- Counter3 value is " + str(counter3))


@task(filePath=FILE_INOUT)
def increment(filePath):
    # Read value
    fis = open(filePath, 'r')
    value = fis.read()
    fis.close()

    # Write value
    fos = open(filePath, 'w')
    fos.write(str(int(value) + 1))
    fos.close()


if __name__ == "__main__":
    main_program()
