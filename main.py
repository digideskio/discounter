#!/usr/bin/env python

"""
Application that returns the most commonly used words in text files

Distributed, multiprocess application that returns a list of most commonly
used words in a text file, or the total accross multiple files.
"""

import sys
import argparse
import logging
import multiprocessing
import lib.wordcounter

__author__ = "Fran Fitzpatrick"
__copyright__ = "Copyright (c) 2015, %s" % __author__
__license__ = "GPLv3"
__version__ = "1.0"
__maintainer__ = __author__
__email__ = "francis.x.fitzpatrick@gmail.com"
__status__ = "Prototype"

class ErrorParser(argparse.ArgumentParser):
    def error(self, message):
        logging.error("error: %s" % message)
        self.print_help()
        sys.exit(2)

description = str("A distributed, multiprocess application that will return the"
                  " most commonly used words in a file (or combination of many "
                  "files).")
parser = ErrorParser(description=description)
parser.add_argument("-f", "--file", type=argparse.FileType('r'), nargs='*',
                    help="File to perform word count on")
parser.add_argument("-c", "--count", help="How many words to display "
                    "(default: %(default)s)", type=int, default=10)
parser.add_argument("-n", "--nprocs", help="The number of local "
                    "processes to spawn. Defaults to how many available "
                    "CPU cores on the current computer (%(default)s).",
                    default=multiprocessing.cpu_count(), type=int)
parser.add_argument("--regex", help="Custom regular expression",
                    default="(\w+)")
parser.add_argument("-v", "--verbose", help="Display debugging log messages", 
                    action="store_true")
parser.add_argument("--ipaddr", help="IP Address", default="127.0.0.1")
parser.add_argument("--port", help="TCP Port", default=31337, type=int)
parser.add_argument("--authkey", default="!QAZxsw2#EDCvfr4%TGBnhy6&UJM",
                    help="The authorization key (or password) that the server "
                    "and workers use to communicate")
parser.add_argument("-w", "--worker", action="store_true",
                    help="Start as just a worker", default=False)
args = parser.parse_args()

if (args.verbose):
    logging.basicConfig(level=logging.DEBUG)

if ((args.worker == False and args.file == None) or
    (args.worker == True and args.file != None)):
    logging.error("You must either run this application as a worker (-w) "
                  "or run with files to process (-f), but not both.")
    parser.print_help()
    
    sys.exit(1)

wc = lib.wordcounter.WordCounter()
wc.count(args.file, amt_of_words=args.count, regex=args.regex,
         nprocs=args.nprocs, ipaddr=args.ipaddr, port=args.port,
         authkey=args.authkey, worker=args.worker)
