#!/usr/bin/env python

import os
import subprocess
import re
import time
import threading

def trace_error_kafka_log(kafka_log_file=None):
    """
    Trace the logfile and and notify if there is any exception/error occurred in kafka
    :param kafka_log_file:
    :return:
    """
    important = []
    keep_phrases = ["ERROR", "EXCEPTION", "FATAL", "error"]

    with open(kafka_log_file) as f:
        f = f.readlines()
    for line in f:
        for phrase in keep_phrases:
            if phrase in line:
                important.append(line)
                break
    if important:
        print(important)


def main():
    kafka_log_file = '/opt/kafka_2.11-0.9.0.0/logs/server.log'
    while 1==1:
        trace_error_kafka_log(kafka_log_file)
        time.sleep(30)

if __name__ == '__main__':
    main()
