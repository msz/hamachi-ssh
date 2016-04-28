#!/usr/bin/env python3
import subprocess
import os
import re


def extract_record(line):
    s = line.split()
    if len(line) <= 3:
        return None
    record = (s[1], s[2]) if s[0] != '*' else (s[2], s[3])
    if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', record[1]) is None:
        return None  # there's no IP where we expect so line does not contain record
    return record

def change_records(ssh_configfiletext):
    records = re.split(r'',ssh_configfiletext)

try:
    process = subprocess.Popen(["hamachi", "list"], stdout=subprocess.PIPE)
except OSError as e:
    if e.errno == os.errno.ENOENT:
        print("Hamachi for Linux is not installed. Get it from https://secure.logmein.com/labs/")
        exit(-1)
    else:
        raise

out, err = process.communicate()
data = out.decode("UTF-8").split('\n')
records = [extract_record(line) for line in data]
records = [r for r in records if r is not None]

