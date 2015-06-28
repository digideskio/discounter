import sys
import argparse
import logging
import multiprocessing
import lib.wordcounter

class ErrorParser(argparse.ArgumentParser):
    def error(self, message):
        logging.error("error: %s" % message)
        self.print_help()
        sys.exit(2)

description = str("A distributed, multiprocess application that will return the"
                  " most commonly used words in a file (or combination of many "
                  "files).")
parser = ErrorParser(description=description)
parser.add_argument("filename", type=argparse.FileType('r'), nargs='+',
                    help="File to perform word count on")
parser.add_argument("-c", "--count", help="How many words to display "
                    "(default: %(default)s)", type=int, default=10)
parser.add_argument("-p", "--processes", help="The number of local "
                    " processes to spawn. Defaults to how many available "
                    "CPU cores on the current computer (%(default)s).",
                    default=multiprocessing.cpu_count(), type=int)
parser.add_argument("--regex", help="Custom regular expression",
                    default="(\w+)")
parser.add_argument("-v", "--verbose", help="Display debugging log messages", 
                    action="store_true")

args = parser.parse_args()

if (args.verbose):
    logging.basicConfig(level=logging.DEBUG)

wc = lib.wordcounter.WordCounter()
wc.count(args.filename, amt_of_words=args.count, regex=args.regex,
         nprocs=args.processes)
