import argparse
import logging
import multiprocessing

description = str("A distributed, multiprocess application that will return the"
                  " most commonly used words in a file (or combination of many "
                  "files.")

logger = logger.getLogger(__name__)
parser = argparse.ArgumentParser(description=description)
parser.add_argument("filename", type=argparse.FileType('r'), nargs='+',
                    help="File to perform word count on")
parser.add_argument("-c", "--count", help="How many words to display "
                    "(default: %(default)s)", type=int, default=10)
parser.add_argument("-re", "--regex", help="Custom regular expression",
                    default="(\w+)")
parser.add_argument("-p", "--processes", help="The number of local "
                    " processes to spawn. Defaults to how many available "
                    "CPU cores on the current computer (%(default)s).",
                    default=multiprocessing.cpu_count(), type=int)
args = parser.parse_args()


