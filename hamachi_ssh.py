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
import sys
import argparse


IP_REGEX = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
DEFAULT_SSH_CONFIG_PATH = os.path.join(os.path.expanduser('~'),
                                       '.ssh/config')


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


def find_records(ssh_configfiletext, records):
    text = ssh_configfiletext
    return [r for r in records
            if re.search(r'\b({0})\b'.format(re.escape(r[0])),
                         text,
                         flags=re.IGNORECASE)
            is not None]


def update_hosts(ssh_configfiletext, records):
    text = ssh_configfiletext
    for r in records:
        text = re.sub(r'(Host +{0}\s.*?Hostname +){1}(\s+.*?(?:\n$|\n\n))'.format(re.escape(r[0]), IP_REGEX),
                      r'\g<1>' + r[1] + r'\g<2>',
                      text,
                      count=1,
                      flags=re.DOTALL)
    return text


def generate_host_for_record(record):
    return ("Host {0}\n"
            "Hostname {1}").format(record[0], record[1])


def generate_hosts_for_records(records):
    return "\n\n".join([generate_host_for_record(r) for r in records])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file",
                        nargs='?',
                        help="the SSH config file to modify",
                        default=DEFAULT_SSH_CONFIG_PATH)
    parser.add_argument("-f", "--force",
                        help="do not prompt for anything",
                        action="store_true")
    args = parser.parse_args()
    config_path = args.file
    force = args.force

    try:
        process = subprocess.Popen(["hamachi", "list"], stdout=subprocess.PIPE)
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            sys.exit("Hamachi for Linux is not installed. " +
                     "Get it from https://secure.logmein.com/labs/")
        else:
            raise

    out, err = process.communicate()
    records = process_hamachi_output(out)

    try:
        with open(config_path, 'r') as f:
            found_file = True
            config = f.read()
    except FileNotFoundError as e:
        found_file = False
        if not force:
            print(("SSH config file at {0} not found. "
                   "Do you want to create it? [y]/n:")
                  .format(DEFAULT_SSH_CONFIG_PATH),
                  end='')
            if input().lower().startswith('n'):
                sys.exit()
            config = ""

    found = find_records(config, records)
    not_found = [r for r in records if r not in found]
    del records

    if len(found)>0:
        config = update_hosts(config, found)
        print("Updated config entries for: " +
              ", ".join(r[0] for r in found) + ".")

    if len(not_found)>0:
        config = "\n\n".join([config, generate_hosts_for_records(not_found)])
        if found_file:
            print("Warning: Entries for: " +
                  ", ".join(r[0] for r in not_found) +
                  " not found. They have been generated for you. ")
        else:
            print("Entries for: " +
                  ", ".join(r[0] for r in not_found) +
                  " have been generated.")
        print("Please fill them out with appropriate information "
              "needed to connect.")

    try:
        with open(config_path, 'w') as f:
            f.write(config)
    except IOError:
        sys.exit("An unexpected error occured "
                 "while trying to write new config file.")

    sys.exit()


if __name__ == '__main__':
    main()
