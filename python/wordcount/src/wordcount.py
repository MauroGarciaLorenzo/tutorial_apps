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
import subprocess
# -*- coding: utf-8 -*-

import sys
import yaml
import os
import time

from pycompss.api.task import task
from pycompss.api.parameter import *


@task(file_path=FILE_IN, returns=list)
def read_file(file_path):
    """ Read a file and return a list of words.
    :param file_path: file's path
    :return: list of words
    """
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data += line.split()
    return data


@task(returns=dict)
def wordCount(data):
    """ Construct a frequency word dictorionary from a list of words.
    :param data: a list of words
    :return: a dictionary where key=word and value=#appearances
    """
    partialResult = {}
    for entry in data:
        if entry in partialResult:
            partialResult[entry] += 1
        else:
            partialResult[entry] = 1
    return partialResult


@task(returns=dict, priority=True)
def merge_two_dicts(dic1, dic2):
    """ Update a dictionary with another dictionary.
    :param dic1: first dictionary
    :param dic2: second dictionary
    :return: dic1+=dic2
    """
    for k in dic2:
        if k in dic1:
            dic1[k] += dic2[k]
        else:
            dic1[k] = dic2[k]
    return dic1


if __name__ == "__main__":
    print("11111111111111111111", flush=True)
    from pycompss.api.api import compss_wait_on

    print("3333311111111111111111111", flush=True)
    # Start counting time...
    start_time = time.time()
    print("2221111111111111111111", flush=True)
    # Get the dataset path
    path_to_yaml = sys.argv[1]
    print("path to yaml:", path_to_yaml, flush=True)
    with open(path_to_yaml, 'r') as file:
        yaml_content = yaml.safe_load(file)

    print("//////////////////////////7", flush=True)
    print(yaml_content, flush=True)
    application_dict = yaml_content.get('application', {})

    print("aplication", application_dict, flush=True)
    pathDataset = application_dict['pathDataset']
    print("path dataset", pathDataset, flush=True)
    if not pathDataset.startswith("/"):
        home_dir = subprocess.run("echo $HOME", shell=True,
                                  capture_output=True,
                                  text=True).stdout.strip()
        pathDataset = os.path.join(home_dir, pathDataset)
    if not os.path.exists(pathDataset):
        raise FileNotFoundError(f"Path dataset {pathDataset} not found")
    else:
        print("Path dataset:", pathDataset, flush=True)

    # Construct a list with the file's paths from the dataset
    paths = []
    for fileName in os.listdir(pathDataset):
        print("FILEEEEEE:", fileName, flush=True)
        paths.append(os.path.join(pathDataset, fileName))

    # Read file's content execute a wordcount on each of them
    partialResult = []
    for p in paths:
        data = read_file(p)
        partialResult.append(wordCount(data))

    # Accumulate the partial results to get the final result.
    result = {}
    for partial in partialResult:
        result = merge_two_dicts(result, partial)

    # Wait for result
    result = compss_wait_on(result)

    elapsed_time = time.time() - start_time

    # Print the results and elapsed time
    print("Word appearances:")
    from pprint import pprint
    pprint(result)
    print("Elapsed Time (s): " + str(elapsed_time))
    print("Words: " + str(sum(result.values())))
