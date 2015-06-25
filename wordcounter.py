import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", type=argparse.FileType('r'), nargs='+',
                    help="File to perform word count on")
parser.add_argument("-c", "--count", help="How many words to display "
                    "(default: %(default)s)", type=int, default=10)
parser.add_argument("-re", "--regex", help="Custom regular expression",
                    default="(\w+)")
args = parser.parse_args()

