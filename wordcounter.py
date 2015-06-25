import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument("file", type=argparse.FileType('r'), nargs='+',
                    help="File to perform word count on")
parser.add_argument("-c", "--count", help="How many words to display "
                    "(default: %(default)s)", type=int, default=10)
parser.add_argument("-re", "--regex", help="Custom regular expression",
                    default="(\w+)")
parser.add_argument("-p", "--processes", help="The number of local "
                    " processes to spawn (default: %(default)s).",
                    default=3, type=int)
args = parser.parse_args()

logger = logger.getLogger(__name__)
