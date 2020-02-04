#!/bin/env python3

import sys
import argparse
import logging
import pprint
from testcases.library import Library
from testcases.expressions import eval_bool

def main(*in_args):
    parser = argparse.ArgumentParser(description='Query and print information about testcases and/or requirements in the testcase library.')
    parser.add_argument(
        'directory',
        help="Directory where requirements and testcases are located.",
    )
    parser.add_argument(
        'query',
        nargs='?',
        default="True",
        help="Jinja expression used for filterling. Use 'i' variable for the item reference. Also 'tc' in case of testcase and 'req' in case of requirement are available.",
    )
    selector = parser.add_mutually_exclusive_group()
    selector.add_argument(
        '-r', '--requirements-only',
        action="store_true",
        help="Show requirements only.",
    )
    selector.add_argument(
        '-t', '--testcases-only',
        action="store_true",
        help="Show testcases only.",
    )
    parser.add_argument(
        '-b', '--brief',
        action="store_true",
        help="Show only list of items without details.",
    )
    ...
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        '-d', '--debug',
        action="store_true",
        help="Turn on debugging.",
    )
    verbosity.add_argument(
        '-q', '--quiet',
        action="store_true",
        help="Run in quiet mode: show errors and failures only.",
    )
    args = parser.parse_args(in_args)
    loglevel = logging.INFO
    logformat = "%(levelname)-8s: %(message)s"
    if args.debug:
        loglevel = logging.DEBUG
        logformat = "%(name)s(%(levelname)s): %(message)s"
    elif args.quiet:
        loglevel = logging.ERROR
    logging.basicConfig(
        level=loglevel,
        format=logformat,
    )
    library = Library(args.directory)
    if not args.testcases_only:
        for requirement in library.requirements.values():
            if eval_bool(args.query, i=requirement, req=requirement):
                if args.brief:
                    print(repr(requirement))
                else:
                    print(requirement.dump())
    if not args.requirements_only:
        for testcase in library.testcases.values():
            if eval_bool(args.query, i=testcase, tc=testcase):
                if args.brief:
                    print(repr(testcase))
                else:
                    print(testcase.dump())

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))