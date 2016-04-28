#!/usr/bin/env python3

"""
The MIT License (MIT)

Copyright (c) 2016 Michał Szewczak

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import subprocess
import os
import re

IP_REGEX = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'


def process_hamachi_output(hamachi_output):
    data = hamachi_output.decode("UTF-8").split('\n')
    records = [extract_record(line) for line in data]
    records = [r for r in records if r is not None]
    return records


def extract_record(line):
    s = line.split()
    if len(line) <= 3:
        return None
    record = (s[1], s[2]) if s[0] != '*' else (s[2], s[3])
    if re.match(IP_REGEX, record[1]) is None:
        return None  # there's no IP where we expect so line does not contain record
    return record


def update_hosts(ssh_configfiletext, records):
    text = ssh_configfiletext
    for r in records:
        text = re.sub(r'(Host +' + re.escape(r[0]) + r'\s.*?Hostname +)'+IP_REGEX + r'(\s+.*?(?:\n$|\n\n))',
                      r'\g<1>' + r[1] + r'\g<2>',
                      text,
                      count=1,
                      flags=re.DOTALL)
    return text


if __name__ == '__main__':
    try:
        process = subprocess.Popen(["hamachi", "list"], stdout=subprocess.PIPE)
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            print("Hamachi for Linux is not installed. Get it from https://secure.logmein.com/labs/")
            exit(-1)
        else:
            raise
    out, err = process.communicate()
    records = process_hamachi_output(out)


