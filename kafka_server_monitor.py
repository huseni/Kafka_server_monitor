#!/usr/bin/env python

# This script is to monitoring the kafka server on the cluster node and if it's down then start it up #
import os
import subprocess
import re
import time
import threading
import time
from functools import wraps


# Fail retry decorator
def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck, e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print msg
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator
    return deco_retry


@retry(Exception, tries=4)
def test_fail(text):
    raise Exception("Fail")


def find_process(process_name):
    ps = subprocess.Popen("ps -eaf | grep "+process_name, shell=True, stdout=subprocess.PIPE)
    output = ps.stdout.read()
    print(" ******************** All kafka processes ******************")
    print (output)
    print(" ******************************************************************************")
    ps.stdout.close()
    ps.wait()
    return output


# This is the function you can use
def is_process_running(process_name ):
    output = find_process(process_name)
    if re.search('server.properties' , output) is None:
        print("couldn't find the kafka running")
        return False
    else:
        return True


# This function will start up the kafka process
def start_kafka_server():
    """
    start kafka process when it finds shutdown
    """
    cmd = '/opt/kafka_2.11-0.9.0.0/bin/kafka-server-start.sh config/server.properties &'
    print("Attempting the start the kafka..... ")
    rc  = os.system(cmd)
    if rc is not 0:
        print("kafka server has been restarted")
    else:
        print("ERROR: kafka server couldn't be restarted")


def trace_error_kafka_log(kafka_log_file=None):
    """
    Check and notify if there is any exception/error occurred in kafka
    :param kafka_log_file:
    :return:
    """
    kafka_log_file = '/opt/kafka_2.11-0.9.0.0/logs/server.log'

    important = []
    keep_phrases = ["ERROR", "EXCEPTION", "FATAL"]

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
    while 1==1:
        if is_process_running('kafka') == False:
            print("Kafka is not running! ")
            start_kafka_server()
        else:
            print("Kafka is running. No worries!")
        time.sleep(5)


if __name__ == '__main__':
    main()

